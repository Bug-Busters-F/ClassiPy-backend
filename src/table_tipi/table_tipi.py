import pandas as pd
import re
import chromadb
from chromadb.utils import embedding_functions
import time

CSV_PATH = "src/table_tipi/tipi.csv"
CHROMA_DB_PATH = "src/database/chroma_db"
COLLECTION_NAME = "ncm_eletronicos"
BATCH_SIZE = 10 

# -------------------------
# Carrega CSV e normaliza
# -------------------------
df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
df["NCM_NORMALIZED"] = df["NCM"].str.replace(".", "", regex=False).str.strip()
df["NCM_DIGITS"] = df["NCM_NORMALIZED"].str.replace(r"\D", "", regex=True)
df["NIVEL"] = df["NCM_DIGITS"].str.len()

descricao_map = dict(zip(df["NCM"], df["Descricao"]))

def find_parent(ncm_digits):
    nivel = len(ncm_digits)
    candidates = df[df["NIVEL"] < nivel]
    for level in sorted(candidates["NIVEL"].unique(), reverse=True):
        subset = candidates[candidates["NIVEL"] == level]
        for _, row in subset.iterrows():
            parent_digits = re.sub(r"\D", "", row["NCM"])
            if ncm_digits.startswith(parent_digits):
                return row["NCM"]
    return ""

df["NCM_PAI"] = df["NCM_DIGITS"].apply(find_parent)

def get_context_chain(ncm, df, descricao_map):
    chain = []
    current = ncm
    while True:
        parent = df.loc[df["NCM"] == current, "NCM_PAI"].values
        desc = descricao_map.get(current, "")
        if desc:
            chain.append(desc)
        if len(parent) == 0 or parent[0] == "":
            break
        current = parent[0]
    return " ".join(reversed(chain))

df_nivel8 = df[df["NIVEL"] == 8].copy()
df_nivel8["Aliquota"] = df_nivel8["Aliquota"].replace("", "0")
df_nivel8["DOCUMENTO"] = df_nivel8.apply(
    lambda row: f"{get_context_chain(row['NCM'], df, descricao_map)} (Alíquota: {row['Aliquota']}%)",
    axis=1
)

ollama_embed = embedding_functions.OllamaEmbeddingFunction(model_name="bge-m3")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=ollama_embed
)

# Limpa coleção existente
try:
    existing = collection.count()
    if existing > 0:
        collection.delete(ids=[str(i) for i in range(existing)])
        print(f"🧹 Coleção limpa ({existing} registros removidos).")
except Exception:
    pass

# -------------------------
# Insere dados em batches pequenos
# -------------------------
for i in range(0, len(df_nivel8), BATCH_SIZE):
    batch = df_nivel8.iloc[i:i+BATCH_SIZE]
    collection.add(
        ids=[str(j) for j in range(i, i + len(batch))],
        documents=batch["DOCUMENTO"].tolist(),
        metadatas=batch[["NCM", "NCM_PAI", "Aliquota"]].to_dict(orient="records")
    )
    print(f"Batch {i//BATCH_SIZE + 1} inserido ({len(batch)} registros).")
    time.sleep(0.5)

print(f"\n✅ Inserção concluída: {len(df_nivel8)} NCMs de 8 dígitos adicionados!")
