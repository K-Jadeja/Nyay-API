import pinecone
from langchain.vectorstores import Pinecone

pinecone.init(
    api_key="f7aa89af-ac99-4619-8914-8d08740f7b38",  # find at app.pinecone.io
    environment="us-east-1-aws"  # next to api key in console
)

index_name = "langchain-demo"

# index = Pinecone.from_documents(docs, embeddings, index_name=index_name)