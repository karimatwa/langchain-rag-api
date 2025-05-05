# LangChain RAG API

This project is a Retrieval-Augmented Generation (RAG) API built using [LangChain](https://www.langchain.com/), OpenAI embeddings, PostgreSQL for vector storage, and Flask for the web API. It allows users to index documents into a vector store and ask natural language questions that are answered using relevant document chunks.

## 📦 Features

- REST API built with Flask
- Document indexing endpoint
- Natural language Q&A using LangChain and OpenAI
- Vector store backed by PostgreSQL
- Dockerized environment for reproducibility

## 🧰 Tech Stack
- Python
- Flask
- LangChain
- OpenAI API
- PostgreSQL + pgvector
- Docker
## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key
- PostgreSQL database (local or remote)

### Clone the Repository

```bash
git clone https://github.com/karimatwa/langchain-rag-api.git
cd langchain
```

### Environment Configuration

```bash
cp example.env .env
```
Set the environment variables.

#### 🐳 Run with Docker

```bash
docker-compose up --build
```

#### 🧪 API Endpoints

## POST `/index`
Trigger indexing of documents into the vector store.

JSON body:
```json
{
  "password": "your_index_password"
}
```

## POST `/ask`
Ask a natural language question.

JSON body:
```json
{
  "question": "What is LangChain?"
}
```

## GET /health
Returns `ready` or `initializing` depending on QA chain readiness.

