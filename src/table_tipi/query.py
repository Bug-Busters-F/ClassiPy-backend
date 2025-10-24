import chromadb
from chromadb.utils import embedding_functions
# -------------------------
# Configurações
# -------------------------
CHROMA_DB_PATH = "src/database/chroma_db"
COLLECTION_NAME = "ncm_eletronicos"
MODEL_NAME = "bge-m3"
TOP_K = 10  # máximo de resultados a serem buscados

# -------------------------
# Inicialização
# -------------------------
print("🔄 Inicializando embedding e cliente ChromaDB...")
ollama_embed = embedding_functions.OllamaEmbeddingFunction(model_name=MODEL_NAME)
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=ollama_embed
)
print(f"Conectado à coleção '{COLLECTION_NAME}' no caminho '{CHROMA_DB_PATH}'.\n")

# -------------------------
# Funções auxiliares
# -------------------------
def interpretar_relevancia(score: float) -> str:
    """Scores mais baixos = mais próximos (mais relevantes)."""
    if score < 0.45:
        return "Alta"
    elif score < 0.48:
        return "Média"
    else:
        return "Baixa"

def resumir_descricao(texto: str, query: str, max_len: int = 200) -> str:
    """Extrai a parte mais relevante da descrição baseada no termo buscado."""
    texto = texto.replace("(Alíquota", "").strip()
    index = texto.lower().find(query.lower())
    if index != -1:
        resumo = texto[index:index+max_len]
    else:
        resumo = texto[:max_len]
    if len(resumo) < len(texto):
        resumo += "..."
    return resumo

# -------------------------
# Função principal de busca
# -------------------------
def search_ncm(query: str, top_k: int = TOP_K):
    print(f"Buscando informações relacionadas a: '{query}'...\n")
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    if not results["ids"] or len(results["ids"][0]) == 0:
        print("Nenhum resultado encontrado.")
        return []
    
    final_results = []

    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        doc = results["documents"][0][i]
        score = results["distances"][0][i]

        ncm = meta.get("NCM", "")
        aliquota = meta.get("Aliquota", "0")

        final_result = {
            "ncm": ncm,
            "descricao_ncm": doc,
            "score": round(score, 4),
            "aliquota": aliquota
        }

        final_results.append(final_result)

    print(f"✅ {len(final_results)} resultados relevantes encontrados!\n")
    return final_results


# -------------------------
# Exemplo de uso
# -------------------------
if __name__ == "__main__":
    termo = "Transistor"
    resultados = search_ncm(termo, top_k=1)
    print(resultados)
