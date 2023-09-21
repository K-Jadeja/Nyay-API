# import pinecone
# import os
# from langchain.vectorstores import Pinecone
# from langchain.embeddings.openai import OpenAIEmbeddings

# model_name = 'text-embedding-ada-002'

# embeddings = OpenAIEmbeddings(
#     model=model_name,
#     openai_api_key="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"
# )

# PINCONE_API_KEY = os.getenv("Pinecone_API_Key") 
# PINECONE_ENV = os.getenv("Pinecone_env") 

# index_name = 'nyay'
# pinecone.init(
#     api_key=PINCONE_API_KEY,
#     environment=PINECONE_ENV
# )

# #
# index = pinecone.Index("nyay")
# vectorstore = Pinecone(index, embeddings.embed_query, "text")

# vectorstore.add_texts(texts)
# # index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
