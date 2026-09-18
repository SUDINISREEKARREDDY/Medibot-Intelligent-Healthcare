# Medibot — AI Medical Chatbot

<<<<<<< HEAD
An AI-powered medical chatbot that uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from a medical reference book and generate responses using a local Large Language Model.

## Overview

Medibot is a Python-based AI application that combines:

- Large Language Models
- Retrieval-Augmented Generation (RAG)
- Vector Search
- Semantic Embeddings
- Pinecone Vector Database
- Flask Web Application
- Local LLM inference with Ollama
=======
An AI-powered medical chatbot that uses Retrieval-Augmented Generation (RAG) to retrieve relevant medical information and generate context-based responses to user health-related queries.

## Overview

Medibot is a Python-based AI application that combines a local Large Language Model (LLM) with a vector database to retrieve relevant information from a medical reference book and generate responses based on the retrieved context.
>>>>>>> 789697b (Update README with RAG and Ollama setup)

The application retrieves relevant medical information from a medical reference book before generating an answer.

<<<<<<< HEAD
## Architecture
=======
- **Python**
- **Flask**
- **LangChain**
- **Ollama**
- **Llama 3.2 3B**
- **Hugging Face Sentence Transformers**
- **Pinecone**
- **Docker**

## How It Works
>>>>>>> 789697b (Update README with RAG and Ollama setup)

```text
User Query
    ↓
Flask Web Application
    ↓
<<<<<<< HEAD
=======
LangChain
    ↓
>>>>>>> 789697b (Update README with RAG and Ollama setup)
Query Embedding
    ↓
Pinecone Vector Search
    ↓
Relevant Medical Context
    ↓
<<<<<<< HEAD
RAG Prompt
    ↓
Ollama
    ↓
Llama 3.2 3B
=======
Llama 3.2 3B via Ollama
>>>>>>> 789697b (Update README with RAG and Ollama setup)
    ↓
Generated Response
```

## RAG Pipeline

The medical reference book is processed into smaller text chunks and converted into vector embeddings using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embeddings are stored in a Pinecone index.

When a user asks a question:

1. The question is received by the Flask application.
2. Relevant medical information is retrieved from Pinecone.
3. The retrieved context is added to the prompt.
4. Llama 3.2 3B generates a response through Ollama.
5. The response is returned through the web interface.

## Key Features

- Retrieval-Augmented Generation (RAG)
- Medical information retrieval using Pinecone
- Sentence Transformer embeddings
- Local LLM inference using Ollama
- Llama 3.2 3B
- Flask-based web interface
- Context-based responses

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SUDINISREEKARREDDY/Medibot-Intelligent-Healthcare.git
cd Medibot-Intelligent-Healthcare
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Start Ollama

Download the required model:

```bash
ollama pull llama3.2:3b
```

Start the Ollama server:

```bash
ollama serve
```

### 5. Configure Pinecone

Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your_pinecone_api_key
```

Never commit or expose your API key.

### 6. Add the Medical Book

Place the medical reference PDF at:

```text
data/Medical_book.pdf
```

### 7. Build the Pinecone Index

```bash
python store_index.py
```

### 8. Run the Application

```bash
python app.py
```

Open the application at:

```text
http://localhost:8080
```

## Project Structure

```text
Medibot-Intelligent-Healthcare/
│
├── app.py
├── store_index.py
├── requirements.txt
├── setup.py
├── Dockerfile
├── README.md
│
├── src/
│   ├── helper.py
│   └── prompt.py
│
├── templates/
│   └── chat.html
│
├── static/
│
└── data/
    └── Medical_book.pdf
```

## Environment Variables

The application requires:

```env
PINECONE_API_KEY=your_pinecone_api_key
```

Never commit API keys or other sensitive credentials.

## Disclaimer

Medibot is an educational AI project and is not a substitute for professional medical advice, diagnosis, or treatment.

For medical concerns, consult a qualified healthcare professional.