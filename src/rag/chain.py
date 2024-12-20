from typing import List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# for typing
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


from src.rag.prompts import (
    course_toc_prompt,
    week_toc_prompt,
    week_item_toc_prompt,
    is_concept_or_project_prompt,
    concept_slide_prompt,
    project_slide_prompt,
    rag_prompt,
    rag_without_question_prompt,
)


def _format_docs(docs: List[Document]):
    return "\n\n".join(doc.page_content for doc in docs)


def get_rag_chain(
    retriever: VectorStoreRetriever, llm: ChatOpenAI
) -> RunnablePassthrough:
    rag_chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_course_toc_chain(retriever: VectorStoreRetriever, llm: ChatOpenAI):
    rag_chain = (
        {
            "context": retriever | _format_docs,
        }
        | rag_without_question_prompt
        | course_toc_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_week_toc_chain(retriever: VectorStoreRetriever, llm: ChatOpenAI):
    rag_chain = (
        {
            "context": retriever | _format_docs,
        }
        | rag_without_question_prompt
        | week_toc_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_week_item_toc_chain(
    retriever: VectorStoreRetriever,
    llm: ChatOpenAI,
):
    rag_chain = (
        {
            "context": retriever | _format_docs,
            "week_name": RunnablePassthrough(),
            "week_item_name": RunnablePassthrough(),
        }
        | rag_without_question_prompt
        | week_item_toc_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_is_concept_or_project_chain(retriever: VectorStoreRetriever, llm: ChatOpenAI):
    rag_chain = (
        {"context": retriever | _format_docs, "key_point": RunnablePassthrough()}
        | rag_without_question_prompt
        | is_concept_or_project_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_concept_slide_chain(retriever: VectorStoreRetriever, llm: ChatOpenAI):
    rag_chain = (
        {"context": retriever | _format_docs, "key_point": RunnablePassthrough()}
        | rag_without_question_prompt
        | concept_slide_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_project_slide_chain(retriever: VectorStoreRetriever, llm: ChatOpenAI):
    rag_chain = (
        {"context": retriever | _format_docs, "project_name": RunnablePassthrough()}
        | rag_without_question_prompt
        | project_slide_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain
