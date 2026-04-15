from chromadb import PersistentClient
from pathlib import Path

DB_NAME = str(Path(__file__).parent / "vector_db_sops")

chroma = PersistentClient(path=DB_NAME)
print([c.name for c in chroma.list_collections()])