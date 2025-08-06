# B3 AI Agent

This project is an AI agent designed to interact with B3's internal APIs and Jira. The agent is built with a backend powered by FastAPI and a lightweight frontend using Streamlit.

## Architecture

The project is divided into a backend and a frontend:

- **Backend**: A FastAPI application that exposes an API for the AI agent. It uses LangChain and CrewAI to orchestrate the agent's logic and interact with external services like Jira and B3's internal APIs.
- **Frontend**: A Streamlit application that provides a simple and interactive user interface for the agent.

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/b3-ai-agent.git
   cd b3-ai-agent
   ```

2. Install the dependencies:
   ```bash
   poetry install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   poetry run uvicorn backend.main:app --reload
   ```

2. In a separate terminal, start the frontend application:
   ```bash
   poetry run streamlit run frontend/app.py
   ```

## Project Structure

```
.
├── backend
│   ├── __init__.py
│   ├── main.py
│   └── core
│       ├── __init__.py
│       └── agent.py
├── frontend
│   └── app.py
├── tests
│   ├── __init__.py
│   └── test_agent.py
├── .gitignore
├── LICENSE
└── README.md
```
