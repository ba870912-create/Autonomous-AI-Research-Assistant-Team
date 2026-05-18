import chromadb
import os

def get_chroma_client():
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
    client = chromadb.PersistentClient(path=persist_dir)
    return client

def get_or_create_collection(collection_name: str = "research_sources"):
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    return collection

def store_source(url: str, content: str, metadata: dict = {}):
    try:
        collection = get_or_create_collection()
        collection.add(
            documents=[content],
            metadatas=[{"url": url, **metadata}],
            ids=[url]
        )
        return True
    except Exception as e:
        print(f"ChromaDB store error: {e}")
        return False

def search_sources(query: str, n_results: int = 5):
    try:
        collection = get_or_create_collection()
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    except Exception as e:
        print(f"ChromaDB search error: {e}")
        return None

def get_all_sources():
    try:
        collection = get_or_create_collection()
        return collection.get()
    except Exception as e:
        print(f"ChromaDB get error: {e}")
        return None