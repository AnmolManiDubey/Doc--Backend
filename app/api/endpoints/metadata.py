from fastapi import APIRouter
from typing import List
from app.models.schemas import DocumentMetadata
from app.db.metadata_store import get_all_metadata

router = APIRouter()

@router.get("/", response_model=List[DocumentMetadata])
async def list_metadata():
    return get_all_metadata()
