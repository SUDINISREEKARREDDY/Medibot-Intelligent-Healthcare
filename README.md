# Medibot — AI Medical Chatbot

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

The application retrieves relevant medical information from a medical reference book before generating an answer.

## Architecture

```text
User Query
    ↓
Flask Web Application
    ↓
Query Embedding
    ↓
Pinecone Vector Search
    ↓
Relevant Medical Context
    ↓
RAG Prompt
    ↓
Ollama
    ↓
Llama 3.2 3B
    ↓
Generated Response
