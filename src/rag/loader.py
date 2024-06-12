from typing import List

from langchain_community.document_loaders import SRTLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import langchain_config

test_splitter = RecursiveCharacterTextSplitter(
    chunk_size=langchain_config.CHUNK_SIZE,
    chunk_overlap=langchain_config.CHUNK_OVERLAP,
    add_start_index=langchain_config.ADD_START_INDEX,
)

def _get_srt_loader(path:str):
    return SRTLoader(path)

def get_documents(path:str) -> List[Document]:
    loader = _get_srt_loader(path)
    document = loader.load()
    chunks = test_splitter.split_documents(document)
    return chunks