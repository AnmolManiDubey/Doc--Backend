def chunk_text(text: str, max_length: int = 500) -> list:
    """
    Split text into chunks of max_length words.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_length):
        chunk = " ".join(words[i:i + max_length])
        chunks.append(chunk)
    return chunks
