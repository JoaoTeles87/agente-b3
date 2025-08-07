import chromadb
from chromadb.utils import embedding_functions
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "b3_collection"

logging.info("Initializing ChromaDB client and embedding function to trigger model download...")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
embedding_function = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)
logging.info("ChromaDB model download should be complete if it wasn't already present.")
logging.info("You can now delete this script (download_chroma_model.py).")