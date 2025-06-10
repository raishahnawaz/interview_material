# Agentic RAG (LangChain Agent) Interview Q&A

## General Questions

**Q: What is the difference between simple RAG and agentic RAG?**
A: Simple RAG retrieves and generates in a single step, while agentic RAG can plan, use tools, and reason over multiple steps (e.g., retrieve, calculate, synthesize).

**Q: What are typical use cases for agentic RAG?**
A: Complex question answering, research assistants, workflow automation, tool-using chatbots, and multi-hop reasoning.

**Q: What are the challenges of agentic RAG?**
A: More complex to implement and debug, requires careful tool design, and can be slower due to multi-step reasoning.

## Code-Specific Questions

**Q: How does the LangChain Agent work in this example?**
A: The agent can use both a retriever tool (to fetch facts) and a calculator tool (to perform computations), orchestrated by the LLM.

**Q: How are tools integrated into the agent?**
A: Tools are defined and passed to the agent; the LLM decides when and how to use them based on the query.

**Q: How would you add more tools or capabilities?**
A: Define new tools (e.g., web search, database query) and add them to the agent's toolset. 