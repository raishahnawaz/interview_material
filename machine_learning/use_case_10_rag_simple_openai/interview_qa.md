# Simple RAG (OpenAI/ChatGPT) Interview Q&A

## General Questions

**Q: How does RAG improve the capabilities of models like ChatGPT?**
A: By grounding answers in retrieved documents, RAG enables ChatGPT to provide more factual, up-to-date, and context-aware responses.

**Q: What frameworks can be used to build RAG pipelines with OpenAI models?**
A: LangChain, LlamaIndex, Haystack, and custom code using OpenAI API and vector databases.

**Q: What are the limitations of using OpenAI models in RAG?**
A: Cost, rate limits, and reliance on external APIs; also, retrieval quality is critical to answer quality.

## Code-Specific Questions

**Q: How does the LangChain RetrievalQA pipeline work in this example?**
A: It uses OpenAI embeddings and FAISS to retrieve relevant documents, then passes them to GPT-3.5/4 for answer generation.

**Q: How is the retriever set up?**
A: Documents are embedded and indexed with FAISS; the retriever finds the most relevant docs for each query.

**Q: How would you add citations or sources to the generated answers?**
A: Modify the prompt or chain to include document metadata, or use LangChain's citation features. 