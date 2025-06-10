# Simple RAG (HuggingFace) Interview Q&A

## General Questions

**Q: What is Retrieval-Augmented Generation (RAG)?**
A: RAG is an architecture that combines information retrieval (fetching relevant documents) with a generative language model to produce grounded, accurate answers.

**Q: What are the main components of a RAG pipeline?**
A: A retriever (e.g., FAISS, DPR) and a generator (e.g., BART, T5, GPT).

**Q: What are the advantages of RAG over pure generation?**
A: RAG can provide up-to-date, factual, and grounded answers by leveraging external knowledge, reducing hallucinations.

## Code-Specific Questions

**Q: How does the HuggingFace RAG pipeline work in this example?**
A: The retriever finds relevant documents from a small knowledge base, and the generator (RAG model) uses those documents to generate an answer.

**Q: How are documents indexed and retrieved?**
A: Documents are indexed using FAISS, and the retriever fetches the most relevant ones for each query.

**Q: How would you scale this to a larger knowledge base?**
A: Use a larger FAISS index or a production vector database, and possibly batch or shard retrieval for efficiency. 