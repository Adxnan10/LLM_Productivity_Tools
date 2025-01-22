"""
Index builder module handles the process of building a vector index for documents using LangChain.
It performs the following tasks: Fetches documents from specified URLs or other sources, Splits documents into manageable chunks for processing,
Embeds the document chunks using a specified embedding model and Stores the embedded chunks in a vector database (Chroma) for retrieval.

At the moment I am only following this guideline: https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/#create-index
TODO: I will change it later to be more modular such that it can be used with other documents.

"""
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List
from config.env_setup import openai_api_key
from constants import ROOT_DIR


def get_embeddings():
    """
    Initialize and return the embedding model.
    """
    return OpenAIEmbeddings(api_key=openai_api_key)


def load_documents(urls: List[str]):
    """
    Load documents from a list of URLs.
    """
    docs = [WebBaseLoader(url).load() for url in urls]
    return [item for sublist in docs for item in sublist]


def split_documents(docs_list: List):
    """
    Split documents into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=0
    )
    return text_splitter.split_documents(docs_list)


def build_and_persist_vectorstore(doc_splits: List, collection_name: str, embd, persist_dir: str):
    """
    Build and persist a vectorstore from document chunks.

    Args:
        doc_splits (List): List of split documents.
        collection_name (str): Name of the vectorstore collection.
        embd: Embedding model to use.
        persist_dir (str): Directory to save the vectorstore.

    Returns:
        Vectorstore: A vectorstore instance.
    """
    os.makedirs(persist_dir, exist_ok=True)
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name=collection_name,
        embedding=embd,
        persist_directory=persist_dir,
    )
    vectorstore.persist()
    return vectorstore


def load_vectorstore(persist_dir: str):
    """
    Load an existing vectorstore from disk.

    Args:
        persist_dir (str): Directory of the saved vectorstore.

    Returns:
        Vectorstore: A loaded vectorstore instance.
    """
    return Chroma(
        collection_name="rag-chroma",
        persist_directory=persist_dir,
        embedding_function=get_embeddings(),
    )


def get_retriever(vectorstore):
    """
    Get a retriever from the vectorstore.
    """
    return vectorstore.as_retriever()

URLS = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

COLLECTION_NAME = "rag-chroma"
PERSIST_DIR = ROOT_DIR + "/vectorstore_data"

# Setup or Load Vectorstore
if not os.path.exists(PERSIST_DIR):
    print("Building and persisting vectorstore...")
    embeddings = get_embeddings()
    documents = load_documents(URLS)
    document_chunks = split_documents(documents)
    vectorstore = build_and_persist_vectorstore(document_chunks, COLLECTION_NAME, embeddings, PERSIST_DIR)
else:
    print("Loading existing vectorstore...")
    vectorstore = load_vectorstore(PERSIST_DIR)

# Get retriever
retriever = get_retriever(vectorstore)