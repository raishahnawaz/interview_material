"""
Simple RAG Example: OpenAI/ChatGPT (via LangChain)
This script demonstrates a retrieval-augmented generation pipeline for document QA using OpenAI's GPT models and LangChain.
"""

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import os

# Set your OpenAI API key (use environment variable for security)
os.environ["OPENAI_API_KEY"] = "sk-..."  # Replace with your key or set externally

# Sample knowledge base (small for demo)
documents = [
    "The Eiffel Tower is located in Paris.",
    "The Great Wall of China is visible from space.",
    "Python is a popular programming language.",
    "The capital of Italy is Rome."
]

# 1. Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(documents, embeddings)

# 2. Setup retriever and LLM
retriever = vectorstore.as_retriever()
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)

# 3. Build RAG pipeline (RetrievalQA)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# 4. User question
question = "Where is the Eiffel Tower?"
result = qa({"query": question})

print(f"Question: {question}")
print(f"Answer: {result['result']}")

# 5. Show retrieved docs
retrieved_docs = retriever.get_relevant_documents(question)
print("\nTop retrieved documents:")
for i, doc in enumerate(retrieved_docs[:2]):
    print(f"Doc {i+1}: {doc.page_content}") 