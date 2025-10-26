import pandas as pd
import re
import chromadb
import time
import uuid
from chromadb.config import Settings
from chromadb.utils import embedding_functions


# ==============================
# CONFIGURAÇÕES GERAIS
# ==============================
CSV_PATH = "src/table_tipi/tipi.csv"
CHROMA_DB_PATH = "src/database/chroma_db"
COLLECTION_NAME = "ncm_eletronicos"
BATCH_SIZE = 10


class ChromaTIPIManager:
    def __init__(self):
        print("[CHROMADB] Inicializando cliente ChromaDB...")
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )

        self.embedding = embedding_functions.OllamaEmbeddingFunction(model_name="bge-m3")
        self.collection = self.get_or_create_collection()
        print("[CHROMADB] Conectado à coleção: {COLLECTION_NAME}")


    def get_or_create_collection(self):
        try:
            print("[CHROMADB] Tentando obter coleção existente...")
            return self.client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=self.embedding
            )
        except Exception:
            print("[CHROMADB] Coleção não encontrada. Criando nova...")
            return self.client.create_collection(
                name=COLLECTION_NAME,
                embedding_function=self.embedding
            )


    def load_and_prepare_csv(self):
        print("[CSV] Carregando arquivo: {CSV_PATH}")
        df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
        df["NCM_NORMALIZED"] = df["NCM"].str.replace(".", "", regex=False).str.strip()
        df["NCM_DIGITS"] = df["NCM_NORMALIZED"].str.replace(r"\D", "", regex=True)
        df["NIVEL"] = df["NCM_DIGITS"].str.len()

        descricao_map = dict(zip(df["NCM"], df["Descricao"]))
        df["NCM_PAI"] = df["NCM_DIGITS"].apply(lambda x: self.find_parent(x, df))
        df["Aliquota"] = df["Aliquota"].replace("", "0")

        df_nivel8 = df[df["NIVEL"] == 8].copy()
        df_nivel8["DOCUMENTO"] = df_nivel8.apply(
            lambda row: f"{self.get_context_chain(row['NCM'], df, descricao_map)} "
                        f"(Alíquota: {row['Aliquota']}%)",
            axis=1
        )

        print(f"[CSV] {len(df_nivel8)} NCMs de 8 dígitos preparados para inserção.")
        return df_nivel8


    def find_parent(self, ncm_digits, df):
        nivel = len(ncm_digits)
        candidates = df[df["NIVEL"] < nivel]
        for level in sorted(candidates["NIVEL"].unique(), reverse=True):
            subset = candidates[candidates["NIVEL"] == level]
            for _, row in subset.iterrows():
                parent_digits = re.sub(r"\D", "", row["NCM"])
                if ncm_digits.startswith(parent_digits):
                    return row["NCM"]
        return ""


    def get_context_chain(self, ncm, df, descricao_map):
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


    def clear_collection(self):
        try:
            existing = self.collection.count()
            if existing > 0:
                print(f"[CHROMADB] Limpando coleção existente ({existing} registros).")
                self.collection.delete(ids=[str(i) for i in range(existing)])
                print(f"[CHROMADB] Coleção limpa com sucesso.")
        except Exception as e:
            print(f"[CHROMADB] Erro ao limpar coleção: {e}")


    def populate_collection(self, batch_size=BATCH_SIZE):
        df = self.load_and_prepare_csv()
        self.clear_collection()

        total_items = len(df)
        print("[CHROMADB] Iniciando inserção de {total_items} registros em lotes de {batch_size}...")

        for i in range(0, total_items, batch_size):
            batch = df.iloc[i:i + batch_size]

            try:
                self.collection.add(
                    ids=[str(uuid.uuid4()) for _ in range(len(batch))],
                    documents=batch["DOCUMENTO"].tolist(),
                    metadatas=batch[["NCM", "NCM_PAI", "Aliquota"]].to_dict(orient="records")
                )
                print("[CHROMADB] Lote {i // batch_size + 1} inserido ({len(batch)} registros).")
                time.sleep(0.5)
            except Exception as e:
                print("[CHROMADB] Erro ao inserir lote: {e}")

        print(f"✅ Inserção concluída: {total_items} NCMs de 8 dígitos adicionados!")


# ==============================
# EXECUÇÃO PRINCIPAL
# ==============================
if __name__ == "__main__":
    manager = ChromaTIPIManager()
    manager.populate_collection()
