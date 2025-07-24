from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.models.schemas import UploadResponse
from app.services.chunker import chunk_text
from app.services.embedder import embed_text
from app.db.vector_store import add_documents
from app.db.metadata_store import save_metadata
import pdfplumber

router = APIRouter()

@router.post("/", response_model=List[UploadResponse])
async def upload_documents(files: List[UploadFile] = File(...)):
    if len(files) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 documents allowed.")
    
    responses = []
    
    for idx, file in enumerate(files):
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
        # Extract text
        text = ""
        with pdfplumber.open(file.file) as pdf:
            if len(pdf.pages) > 1000:
                raise HTTPException(status_code=400, detail=f"{file.filename} exceeds 1000 pages.")
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        # Chunk
        chunks = chunk_text(text)
        
        # Embed
        embeddings = embed_text(chunks)
        
        # Store in vector DB
        metadatas = [{"filename": file.filename}] * len(chunks)
        add_documents(chunks, embeddings, metadatas, doc_id_prefix=f"{file.filename}_{idx}")
        
        # Save metadata
        save_metadata(file.filename, len(chunks))
        
        responses.append(UploadResponse(
            filename=file.filename,
            num_chunks=len(chunks),
            message="Uploaded & processed successfully"
        ))
    return responses
