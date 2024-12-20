from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import VectorStoreRetriever

from .loader import get_documents
from .vector_database import get_langchain_chroma
from .embedding import openai_embedding
from ..log import get_logger, rich_print
from src.config import runtime_config


def save_file(
    collection_name: str,
    path: str,
):
    documents = get_documents(path)
    langchain_chroma = get_langchain_chroma(
        collection_name=collection_name,
        embeddings=openai_embedding,
    )
    # update the database
    if runtime_config.VERBOSE:
        rich_print(
            f"Adding documents [bold]{path.split('/')[-1]}[/bold] to collection [bold]{collection_name}[/bold]"
        )
    else:
        rich_print(f"Processing [bold]{path.split('/')[-1]}[/bold]")

    try:
        langchain_chroma.add_documents(documents=documents)
    except Exception as e:
        rich_print(f"Error adding documents to collection {collection_name}")
        rich_print(e)
        return


def get_retriever(
    collection_name: str,
) -> VectorStoreRetriever:
    get_logger().debug(f"Getting retriever from {collection_name}")
    langchain_chroma = get_langchain_chroma(
        collection_name=collection_name,
        embeddings=openai_embedding,
    )
    return langchain_chroma.as_retriever()


def get_llm():
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    return llm
