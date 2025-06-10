# Use Case 10b: Simple RAG with OpenAI/ChatGPT

This use case demonstrates Retrieval-Augmented Generation (RAG) for document-grounded question answering using OpenAI's ChatGPT (via LangChain or LlamaIndex).

## What is RAG?
RAG combines a retriever (fetches relevant documents/passages) with a generator (language model) to answer questions with up-to-date, grounded information.

## Architecture
- **Retriever**: Finds relevant documents from a knowledge base (e.g., using vector search).
- **Generator**: Uses ChatGPT (or GPT-3.5/4) to generate an answer based on retrieved docs.

## This Example Covers
- Setting up a simple RAG pipeline with OpenAI and LangChain/LlamaIndex
- Using a small set of documents for QA
- Running the pipeline in a containerized environment

See `code/rag_openai_example.py` for the implementation. 