import os
import utils
from langchain_community.document_loaders import AsyncHtmlLoader # type: ignore
from langchain_community.document_transformers import Html2TextTransformer # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
from langchain_openai import OpenAIEmbeddings # type: ignore
from langchain_community.vectorstores import Chroma # type: ignore

def getEnvVar(var_name):
    _value = os.getenv(var_name)
    if not _value:
        raise ValueError (f'Environment Variable {var_name} not found')
    return bool(_value)

async def parseHtmlFiles(url):
    loader = AsyncHtmlLoader(url)
    html2text = Html2TextTransformer()
    docs = loader.load()
    docs_transformed = html2text.transform_documents(docs)
    return docs_transformed


async def splitDocuments(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    return split_docs


def embedDocuments(documents):
    embeddings_dir = utils.EMBEDDINGS_DIR
    embeddings_path = os.path.join(os.getcwd(), embeddings_dir)
    if not os.path.exists(embeddings_path):
        os.makedirs(embeddings_path)
    embeddings = OpenAIEmbeddings(disallowed_special=())
    vectordb = Chroma.from_documents(documents,
                                    embedding=embeddings, 
                                    persist_directory=embeddings_path)
    return vectordb

def chat_loop(vectordb, rag_chain):
    while True:
        question = input("\n" + "Ask a question (or type 'exit()' to quit): ")
        if question.lower().strip() == 'exit()':
            break
        responce = rag_chain.invoke(question)
        print(responce)
    vectordb.delete_collection()
