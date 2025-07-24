import chromadb

client = chromadb.PersistentClient(path="./vector_db")
collection = client.get_or_create_collection(name="documents")

def add_documents(chunks: list, embeddings: list, metadatas: list, doc_id_prefix: str):
    ids = [f"{doc_id_prefix}_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
