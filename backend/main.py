import logging
from fastapi import FastAPI
from pydantic import BaseModel
from core.agent import Agent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query(request: QueryRequest):
    """
    Receives a query and returns a response from the agent.
    """
    logging.info(f"Received request for /query with query: {request.query}")
    agent = Agent()
    response = agent.run(request.query)
    logging.info("Response generated successfully.")
    return {"response": response}

@app.get("/")
def read_root():
    return {"message": "Agent API is running. Use the /query endpoint."}
