import os
from uuid import uuid4
import chromadb

_client: chromadb.ClientAPI = None
_collection = None

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "chroma")


def init_chromadb():
    global _client, _collection
    os.makedirs(CHROMA_PATH, exist_ok=True)
    _client = chromadb.PersistentClient(path=CHROMA_PATH)
    _collection = _client.get_or_create_collection("conversations")


def store(session_id: str, user_msg: str, assistant_msg: str, intent: str):
    if _collection is None:
        return
    doc = f"User: {user_msg}\nAssistant: {assistant_msg}"
    _collection.add(
        documents=[doc],
        metadatas=[{"session_id": session_id, "intent": intent}],
        ids=[f"{session_id}-{uuid4()}"],
    )


def retrieve(session_id: str, query: str, n_results: int = 3) -> list[str]:
    if _collection is None:
        return []
    try:
        count = _collection.count()
        if count == 0:
            return []
        results = _collection.query(
            query_texts=[query],
            n_results=min(n_results, count),
            where={"session_id": session_id},
        )
        return results["documents"][0] if results["documents"] else []
    except Exception:
        return []
