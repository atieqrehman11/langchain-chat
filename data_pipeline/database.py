from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from .embedding import get_embedding_function
from .splitter import split_by_recursive_splitter

persist_directory = 'resources/chroma/'

def load_db(file_path):
    # 1. load the documents
    print("Loading pdf documents")

    pdfs = load_documents(file_path)

    # 2. split
    splits = split_by_recursive_splitter(pdfs, 1500, 150)

    # 3. persist in vector db (embedding will automatically be created by chroma)
    db = persist_docs(splits, OpenAIEmbeddings())

    return db
    
def load_documents(path):
    docs = []
    loader = PyPDFLoader(path)
    docs.extend(loader.load())

    print("Total Pdfs: ", len(docs))
    
    return docs

def persist_docs(splits, embeddings): 
    vectordb = Chroma.from_documents(
        documents = splits,
        embedding = embeddings,
        persist_directory = persist_directory
    )

    print('DB Collection Count: ', vectordb._collection.count())

    return vectordb
