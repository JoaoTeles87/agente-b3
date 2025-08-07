import logging
import chromadb
from chromadb.utils import embedding_functions
from backend.core.oci_client import get_llama2_completion

# --- Constants ---
CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "b3_collection"
# --- ChromaDB Initialization ---
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
embedding_function = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)

def query_rag(query: str, n_results: int = 3) -> str:
    """
    Queries the ChromaDB for relevant documents and generates a response using LLaMA2.
    """
    logging.info(f"Querying RAG with: {query}")

    # 1. Retrieve relevant documents from ChromaDB
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    documents = results['documents'][0]
    logging.debug(f"Retrieved documents: {documents}")

    # 2. Construct the prompt for LLaMA2
    context = "\n".join(documents)
    prompt = f"""Use the following context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {query}

Answer:"""
    logging.debug(f"Generated prompt: {prompt}")

    # 3. Get the completion from the OCI LLaMA2 model
    response = get_llama2_completion(prompt)
    answer = response['choices'][0]['text']
    logging.info(f"LLaMA2 response: {answer}")

    return answer

if __name__ == '__main__':
    # Example usage
    test_query = "What are the minimum infrastructure requirements for SINACOR?"
    response = query_rag(test_query)
    print(f"\n--- Query ---\n{test_query}\n\n--- Answer ---\n{response}")
