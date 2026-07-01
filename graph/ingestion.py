from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def create_retriever(urls):
    docs_list = []
    for url in urls:
        docs_list.extend(WebBaseLoader(url).load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=25)
    splits = text_splitter.split_documents(docs_list)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        collection_name="financial-risk-analyst-agent-chroma",
        persist_directory="./.chroma")

    retriever = vectorstore.as_retriever()

    return retriever

