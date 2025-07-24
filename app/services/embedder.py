from sentence_transformers import SentenceTransformer

# Load local embedding model (downloaded on first run)
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(texts: list) -> list:
    """
    Generate embeddings for a list of texts.
    Returns list of vectors.
    """
    return model.encode(texts).tolist()
