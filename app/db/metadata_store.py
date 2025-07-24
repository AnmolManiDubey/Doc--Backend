from datetime import datetime

metadata_store = []

def save_metadata(filename: str, num_chunks: int):
    metadata_store.append({
        "filename": filename,
        "upload_date": datetime.utcnow().isoformat(),
        "num_chunks": num_chunks
    })

def get_all_metadata():
    return metadata_store
