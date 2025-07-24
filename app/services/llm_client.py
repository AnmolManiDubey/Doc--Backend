from openai import OpenAI
from app.core.config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL

# Initialize OpenAI client with Groq-compatible endpoint
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_BASE_URL
)

def generate_answer(query: str, context_chunks: list) -> str:
    """
    Calls Llama 70B on Groq to generate an answer given the query and context.
    """
    # Concatenate context
    context = "\n\n".join(context_chunks)
    
    prompt = f"""You are an expert assistant.
Answer the following user question based only on the provided context.
If the answer isn't in the context, say "I don't know based on the documents."

Context:
{context}

Question:
{query}

Answer:"""
    
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content.strip()
