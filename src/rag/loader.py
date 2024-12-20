from typing import List

from langchain_community.document_loaders import SRTLoader, BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import langchain_config
from src.config import runtime_config

test_splitter = RecursiveCharacterTextSplitter(
    chunk_size=langchain_config.CHUNK_SIZE,
    chunk_overlap=langchain_config.CHUNK_OVERLAP,
    add_start_index=langchain_config.ADD_START_INDEX,
)


def get_documents(path: str) -> List[Document]:
    if path.endswith(".srt"):
        loader = SRTLoader(path)
    elif path.endswith(".html"):
        loader = BSHTMLLoader(path)
    document = loader.load()
    chunks = test_splitter.split_documents(document)

    if runtime_config.VERBOSE:
        print(f"Splitting {path} into {len(chunks)} chunks")
    return chunks
