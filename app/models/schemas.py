from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    filename: str
    num_chunks: int
    message: str

class DocumentMetadata(BaseModel):
    filename: str
    upload_date: str
    num_chunks: int
