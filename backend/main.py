import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.agent import Agent
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    query: str
    chat_history: Optional[List[Message]] = None

class QueryResponse(BaseModel):
    response: str
    chat_history: List[Message]

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Receives a query and returns a response from the agent.
    """
    logging.info(f"Received request for /query with query: {request.query}")
    chat_history = request.chat_history if request.chat_history is not None else []

    # Add user query to chat history
    chat_history.append(Message(role="user", content=request.query))

    try:
        agent = Agent()
        agent_response = agent.run(request.query, chat_history)
        logging.info("Response generated successfully.")

        # Add agent response to chat history
        chat_history.append(Message(role="agent", content=agent_response))

        return QueryResponse(response=agent_response, chat_history=chat_history)
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")

frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
