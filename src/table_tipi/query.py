import chromadb

CHROMA_DB_PATH = "src/database/chroma_db"
COLLECTION_NAME = "ncm_eletronicos"

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

def search_ncm(query: str, top_k: int = 1):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    responses = []
    for i in range(len(results["ids"][0])):
        response = {
            "id": results["ids"][0][i],
            "NCM": results["metadatas"][0][i]["NCM"],
            "NCM_PAI": results["metadatas"][0][i]["NCM_PAI"],
            "Aliquota": results["metadatas"][0][i]["Aliquota"],
            "Documento": results["documents"][0][i],
            "score": results["distances"][0][i]
        }
        responses.append(response)

    return responses


# -------------------------
# EXEMPLO DE USO
# -------------------------
if __name__ == "__main__":
    query_text = "Aspirador de pó elétrico 3000W"
    results = search_ncm(query_text)

    print(f"\n🔍 Consulta: {query_text}\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. NCM: {r['NCM']} | Pai: {r['NCM_PAI']} | Alíquota: {r['Aliquota']}%")
        print(f"   Documento: {r['Documento']}")
        print(f"   Score (similaridade): {r['score']}\n")
