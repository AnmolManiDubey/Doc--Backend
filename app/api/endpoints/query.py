from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.embedder import embed_text
from app.db.vector_store import collection
from app.services.llm_client import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/")
async def ask_question(payload: QueryRequest):
    query = payload.query
    # Embed the query
    query_embedding = embed_text([query])[0]
    
    # Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5  # adjust top-k as needed
    )
    
    retrieved_chunks = results['documents'][0]
    
    if not retrieved_chunks:
        raise HTTPException(status_code=404, detail="No relevant context found.")
    
    # Call LLM
    answer = generate_answer(query, retrieved_chunks)
    return {"answer": answer}
