# Use Case 10c: Agentic RAG (LangChain Agent)

This use case demonstrates an agentic Retrieval-Augmented Generation (RAG) architecture, where an agent can retrieve, reason, and use tools to answer complex queries.

## What is Agentic RAG?
Agentic RAG extends simple RAG by allowing the model to plan, use tools (retrievers, calculators, APIs), and reason over multiple steps.

## Architecture
- **Agent**: Orchestrates retrieval, reasoning, and tool use (e.g., via LangChain Agent or OpenAI function-calling).
- **Retriever**: Finds relevant documents/passages.
- **Tools**: May include search, calculators, APIs, etc.
- **Generator**: Uses a language model to synthesize answers.

## This Example Covers
- Setting up an agentic RAG pipeline with LangChain
- Demonstrating multi-step reasoning and tool use
- Running the pipeline in a containerized environment

See `code/rag_agentic_example.py` for the implementation. 