# Agente de IA para B3 com RAG

Este projeto é um agente de IA que utiliza a técnica de Geração Aumentada por Recuperação (RAG) para responder a perguntas com base em uma base de conhecimento de documentos. O agente é construído com um backend em FastAPI, utiliza o ChromaDB como banco de dados vetorial e se integra com os modelos de linguagem da OCI (Oracle Cloud Infrastructure) Generative AI.

## Arquitetura

O fluxo do agente segue o padrão RAG:

1.  **Consulta do Usuário**: O usuário envia uma pergunta através da API.
2.  **Recuperação de Documentos**: O sistema busca por documentos relevantes na base de dados vetorial (ChromaDB) que correspondam à consulta do usuário.
3.  **Construção do Prompt**: Os documentos recuperados são inseridos como contexto em um prompt, juntamente com a pergunta original do usuário.
4.  **Geração da Resposta**: O prompt enriquecido é enviado para o modelo de linguagem (LLaMA 2) na OCI Generative AI, que gera uma resposta fundamentada nos documentos fornecidos.

## Como Começar

### Pré-requisitos

- Python 3.9+
- Pip
- Uma conta na Oracle Cloud Infrastructure (OCI) com as credenciais da API configuradas corretamente no seu ambiente local (normalmente em `~/.oci/config`).

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/JoaoTeles87/agente-b3.git
   cd agente-b3
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente. Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis:
   ```dotenv
   COMPARTMENT_ID="seu-compartment-ocid"
   ENDPOINT="seu-service-endpoint"
   LLAMA2_MODEL_OCID="seu-modelo-ocid"
   ```
   Substitua os valores pelos dados correspondentes da sua conta OCI.

## Executando a Aplicação

1. Inicie o servidor backend:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. A API estará disponível em `http://127.0.0.1:8000`. Você pode interagir com ela através da documentação do Swagger UI em `http://127.0.0.1:8000/docs`.

## Estrutura do Projeto

```
.
├── backend
│   ├── main.py
│   └── core
│       ├── agent.py
│       ├── oci_client.py
│       └── rag.py
├── documents
│   └── (coloque seus documentos aqui)
├── chroma_db
│   └── (banco de dados vetorial)
├── .gitignore
├── requirements.txt
└── README.md
```