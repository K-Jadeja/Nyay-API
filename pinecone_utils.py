import pinecone_utils
import os
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

model_name = 'text-embedding-ada-002'

embeddings = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

PINCONE_API_KEY = os.getenv("PINCONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

# Check if environment variables are set
if not PINCONE_API_KEY or not PINECONE_ENV:
    raise ValueError("Pinecone API key or environment not set in environment variables.")

pinecone_utils.init(
    api_key=PINCONE_API_KEY,
    environment=PINECONE_ENV
)

# Initialize the index
index = pinecone_utils.Index("nyay")

# Upsert article to vectorstore
def upsert_doc(texts):
    vectorstore = Pinecone(index, embeddings.embed_query, "text")
    vectorstore.add_texts(texts)
