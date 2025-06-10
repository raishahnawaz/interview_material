"""
Agentic RAG Example: LangChain Agent
This script demonstrates an agentic retrieval-augmented generation pipeline with multi-step reasoning and tool use (retriever + calculator) using LangChain.
"""

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
import os

# Set your OpenAI API key (use environment variable for security)
os.environ["OPENAI_API_KEY"] = "sk-..."  # Replace with your key or set externally

# Sample knowledge base (small for demo)
documents = [
    "The Eiffel Tower is located in Paris.",
    "The Great Wall of China is visible from space.",
    "Python is a popular programming language.",
    "The capital of Italy is Rome.",
    "The height of the Eiffel Tower is 300 meters."
]

# 1. Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(documents, embeddings)
retriever = vectorstore.as_retriever()

# 2. Create retriever tool
retriever_tool = create_retriever_tool(
    retriever,
    "doc_search",
    "Searches documents for relevant information."
)

# 3. Create a simple calculator tool
from langchain.tools import tool
@tool
def calculator_tool(expression: str) -> str:
    """Evaluates a simple math expression."""
    try:
        return str(eval(expression))
    except Exception:
        return "Error evaluating expression."

# 4. Setup LLM and agent
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)
tools = [retriever_tool, calculator_tool]
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# 5. User question (requires both retrieval and calculation)
question = "What is the height of the Eiffel Tower in feet? (1 meter = 3.281 feet)"
result = agent.run(question)

print(f"Question: {question}")
print(f"Agentic RAG Answer: {result}") 