import logging
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Any
from core.rag import initialize_rag, search_documents
from core.agent import Agent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Global variable to hold the FAISS vector store
collection = None

@app.on_event("startup")
def startup_event():
    """
    Initializes the RAG setup when the application starts.
    """
    global collection
    logging.info("Starting up and initializing RAG...")
    collection = initialize_rag()
    logging.info("RAG initialization complete.")

class QueryRequest(BaseModel):
    query: str

class SuggestionRequest(BaseModel):
    query: str
    input_json: Dict[str, Any]
    weights: Dict[str, Any]

@app.post("/enhance-prompt")
async def enhance_prompt(request: QueryRequest):
    """
    Receives a query, finds relevant documents using RAG,
    and returns an enriched prompt.
    """
    logging.info(f"Received request for /enhance-prompt with query: {request.query}")
    if collection is None:
        logging.error("RAG system not initialized.")
        return {"error": "RAG system not initialized"}, 500

    query = request.query
    relevant_docs = search_documents(query, collection)

    # Enrich the prompt with the retrieved documents
    context = "\n\n".join(relevant_docs)
    enriched_prompt = f"Context from documents:\n{context}\n\nUser query: {query}"

    logging.info("Enriched prompt created successfully.")
    return {"enriched_prompt": enriched_prompt}

@app.post("/get-suggestion")
async def get_suggestion(request: SuggestionRequest):
    """
    Receives a query, input JSON, and weights, gets a suggestion from the agent.
    """
    logging.info(f"Received request for /get-suggestion with query: {request.query}")
    if collection is None:
        logging.error("RAG system not initialized.")
        return {"error": "RAG system not initialized"}, 500

    agent = Agent()
    suggestion = agent.run(
        query=request.query,
        input_json=request.input_json,
        weights=request.weights,
        collection=collection
    )

    logging.info("Suggestion generated and sent to Teams successfully.")
    return {"suggestion": suggestion}


@app.get("/")
def read_root():
    return {"message": "RAG API is running. Use endpoints /enhance-prompt and /get-suggestion"}