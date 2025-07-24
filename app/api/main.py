from fastapi import FastAPI
from app.api.endpoints import upload, query, metadata
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "RAG Pipeline",
    description="Retrieval-Augmented Generation Pipeline",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(metadata.router, prefix="/metadata", tags=["Metadata"])

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Pipeline API"}