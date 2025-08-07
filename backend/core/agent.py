import logging
from core.rag import query_rag
from core.oci_client import get_llama2_completion
from typing import List

class Agent:
    def run(self, query: str, chat_history: List[dict] = None) -> str:
        if chat_history is None:
            chat_history = []

        simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "oi"]

        if query.lower() in simple_greetings:
            logging.info("Simple greeting detected. Bypassing RAG and calling OCI directly.")
            # Construct a simple prompt for the OCI model for greetings
            greeting_prompt = f"Você é um assistente de IA amigável especializado em arquitetura de software. Responda à saudação: '{query}' em português."
            response = get_llama2_completion(greeting_prompt)
            return response['choices'][0]['text']
        else:
            # Pass both the current query and the chat history to query_rag
            return query_rag(query, chat_history)
