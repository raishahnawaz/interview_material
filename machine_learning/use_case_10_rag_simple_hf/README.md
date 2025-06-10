# Use Case 10a: Simple RAG with HuggingFace Transformers

This use case demonstrates Retrieval-Augmented Generation (RAG) for document-grounded question answering using HuggingFace Transformers.

## What is RAG?
RAG combines a retriever (fetches relevant documents/passages) with a generator (language model) to answer questions with up-to-date, grounded information.

## Architecture
- **Retriever**: Finds relevant documents from a knowledge base (e.g., using DPR or FAISS).
- **Generator**: Uses a language model (e.g., BART, T5) to generate an answer based on retrieved docs.

## This Example Covers
- Setting up a simple RAG pipeline with HuggingFace
- Using a small set of documents for QA
- Running the pipeline in a containerized environment

See `code/rag_hf_example.py` for the implementation. 