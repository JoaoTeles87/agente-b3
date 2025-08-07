from core.rag import query_rag

class Agent:
    def run(self, query: str) -> str:
        return query_rag(query)
