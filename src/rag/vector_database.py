"""
reference: 
https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
"""
from typing import List

from langchain_chroma import Chroma
import chromadb

from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document

from ..config import chroma_config
from src.log import rich_print, get_logger


def get_chroma_client():
    return chromadb.HttpClient(
        host=chroma_config.HOST,
        port=chroma_config.PORT,
    )


def create_collection(collection_name: str, chroma_client: ClientAPI | None):
    if not chroma_client:
        chroma_client = get_chroma_client()
    _ = chroma_client.get_or_create_collection(collection_name)
    return


def check_collection(collection_name: str, chroma_client: ClientAPI | None):
    if not chroma_client:
        chroma_client = get_chroma_client()
    return collection_name in chroma_client.list_collections()


def delete_collection(collection_name: str, chroma_client: ClientAPI | None):
    if not chroma_client:
        chroma_client = get_chroma_client()
    # check if collection exists
    logger = get_logger()
    logger.debug(f"Checking if collection {collection_name} exists")
    logger.debug(chroma_client.list_collections())
    exist = collection_name in chroma_client.list_collections()
    if not exist:
        rich_print(
            f"[bold][red]ERROR[/red][/bold] Collection [bold]{collection_name}[/bold] does not exist."
        )
        return

    # delete the collection
    rich_print(
        f"Are you sure you want to delete collection [bold]{collection_name}[/bold] ? (y/n)"
    )
    user_check = input()
    if user_check != "y":
        rich_print("Aborted.")
        return
    chroma_client.delete_collection(collection_name)
    rich_print(f"Collection [bold]{collection_name}[/bold] deleted.")

    logger.debug("Checking reamining collections")
    logger.debug(chroma_client.list_collections())


def get_langchain_chroma(
    collection_name: str, embeddings: Embeddings, chroma_client: ClientAPI | None
):
    if not chroma_client:
        chroma_client = get_chroma_client()
    # create a collection if it does not exist
    _ = create_collection(collection_name=collection_name, chroma_client=chroma_client)

    return Chroma(
        client=chroma_client,
        collection_name=collection_name,
        embedding_function=embeddings,
    )


def get_lanchain_chroma_from_document(
    collection_name: str,
    documents: List[Document],
    embeddings: Embeddings,
    chroma_client: ClientAPI | None,
):
    if not chroma_client:
        chroma_client = get_chroma_client()
    # create a collection if it does not exist
    _ = create_collection(collection_name=collection_name, chroma_client=chroma_client)

    return Chroma.from_documents(
        documents=documents,
        collection_name=collection_name,
        embedding_function=embeddings,
        client=chroma_client,
    )
