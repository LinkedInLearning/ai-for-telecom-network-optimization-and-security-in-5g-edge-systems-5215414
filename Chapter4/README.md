Step 1: Install Required Packages
------------------------------------

!pip install -U langchain langchain-community chromadb sentence-transformers openai gradio


Step 2: Set Your Groq API Key
------------------

import os
from openai import OpenAI

os.environ["GROQ_API_KEY"] = "your-groq-api-key"  # Replace with your real key

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)


Step 3: Upload and Parse NRF Logs
--------------------------------------

from google.colab import files
from langchain.docstore.document import Document
import re

uploaded = files.upload()
log_file = next(iter(uploaded))

documents = []
with open(log_file, "r") as f:
    for line in f.readlines():
        match = re.match(r"(\d{4}-\d{2}-\d{2}T[^\s]+)\s\[INFO\]\[NRF\]\[GIN\]\s\|\s(\d{3})\s\|\s([\d\.]+)\s\|\s([A-Z]+)\s\|\s([^|]+)", line)
        if match:
            documents.append(Document(
                page_content=line.strip(),
                metadata={
                    "timestamp": match.group(1),
                    "status_code": match.group(2),
                    "ip": match.group(3),
                    "method": match.group(4),
                    "endpoint": match.group(5)
                }
            ))

Step 4: Setup Chroma Vector Store
---------------------------------------

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(documents, embedding_model)
retriever = db.as_retriever()


Step5: Custom LangChain-Compatible Wrapper for Groq Client
-------------------------------------------------------------

def get_contextual_rag_prompt(query: str, context_docs: list) -> str:
    context = "\n".join([doc.page_content for doc in context_docs])
    return f"""
You are a 5G security analyst analyzing NRF logs.

CONTEXT:
{context}

QUESTION:
{query}

Provide a detailed RCA with actionable insights.
""".strip()

Step 6: Retrieve, Generate RCA Using Groq + LLaMA3
--------------------------------------------------

# Sample RCA query
query = "Explain why IP 10.100.200.1 caused an NRF fault"

# Retrieve top documents
relevant_docs = retriever.get_relevant_documents(query)

# Build the final prompt
final_prompt = get_contextual_rag_prompt(query, relevant_docs)

# Call Groq LLaMA3 model
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "system", "content": "You are an expert in 5G NRF log analysis."},
        {"role": "user", "content": final_prompt}
    ]
)

print("📍 Root Cause Analysis:\n")
print(response.choices[0].message.content)


Sample questions to ask

qa_2 = "Which IPs accessed unauthorized endpoints?"
qa_3 = "Summarize deletion attempts on NRF instances."
qa_4 = "What fault patterns were caused by 5xx errors?"



| Library                             | Purpose                                            |
| ----------------------------------- | -------------------------------------------------- |
| `langchain` + `langchain-community` | Core RAG framework + integrations                  |
| `chromadb`                          | In-memory vector store for fast document retrieval |
| `sentence-transformers`             | Embedding models for turning text into vectors     |
| `openai`                            | OpenAI client (compatible with Groq API)           |
| `gradio`                            | Lightweight chatbot UI framework for Colab or web  |


