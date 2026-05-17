import chromadb
from chromadb.utils import embedding_functions
import os

def get_chroma_collection(name: str = "research_sources"):
    client = chromadb.PersistentClient(
        path=os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
    )
    ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
    return client.get_or_create_collection(name, embedding_function=ef)

def store_source(url: str, content: str, metadata: dict):
    collection = get_chroma_collection()
    collection.add(
        documents=[content],
        metadatas=[{"url": url, **metadata}],
        ids=[url]
    )

def query_sources(query: str, n_results: int = 5) -> list:
    collection = get_chroma_collection()
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]