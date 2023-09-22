import pinecone
import os
from dotenv import load_dotenv
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()
PINCONE_API_KEY = os.environ.get("PINCONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

model_name = 'text-embedding-ada-002'
embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-3.5-turbo',
    temperature=0.0
)

if not PINCONE_API_KEY or not PINECONE_ENV:
    raise ValueError("Pinecone API key or environment not set in environment variables.")
pinecone.init(
    api_key=PINCONE_API_KEY,
    environment=PINECONE_ENV
)
# Initialize the index
index = pinecone.Index("nyay-index")

text_field = "text"

# switch back to normal index for langchain
index = pinecone.Index("nyay-index")

vectorstore = Pinecone(
    index, embed.embed_query, text_field
)

# Upsert article to vectorstore
def upsert_doc(texts):
    vectorstore = Pinecone(index, embed.embed_query, "text")
    vectorstore.add_texts(texts)

# def get_similiar_docs(query,k=2,score=False):
#   if score:
#     similar_docs = index.similarity_search_with_score(query,k=k)
#   else:
#     similar_docs = index.similarity_search(query,k=k)
#   return similar_docs

template = """You are 'Legal.ly', a helpful Know-your-rights bot and legal advisor.
Use the following pieces of context to answer the question at the end. 
If the context does not have the answer, make up a most appropriate and helpful and descriptive answer for an indian. 
You are only supposed to answer law and rights related questons. 
Always remember to use the context to give more information to the user about the law and their rights and consequences.
Decline politely if the question is outside your domain.
Always answer in the language of the question. 
Context: {context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

def retrieve_answer(query):
    result = qa_chain.run(query)
    print("=============================================================")
    return result#["result"]