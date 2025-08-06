from backend.core.agent import Agent

def test_agent():
    agent = Agent()
    response = agent.run("test query")
    assert isinstance(response, str)
