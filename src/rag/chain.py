from typing import List
from operator import itemgetter

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

# for typing
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


from src.rag.core import get_retriever


course_toc_template = """
Give the whole course table of content in markdown list format.

for example:
```
- Week 0: Introduction video, CodeSkulptor, Python arithmetic expressions, practice exercises, variables, Code Sculptor, practice exercises, quiz
- Week 1: Quiz, rock paper scissors lizard Spock mini project
- Week 2: Guess the number game
- Week 3: Digital stopwatch game
- Week 4: Pong game 
```
"""
course_toc_prompt = PromptTemplate.from_template(course_toc_template)

week_toc_template = """
- You are Python Expert and Coursera Assistant.
- Give each 3~5 title in {week_name} week in markdown list format.
- The title should be related to the key points of the week.
- And should not be in {previous_weeks_toc} list .

for example:

```
- expressions
- variables and assignment
- mini project: we want a shrubbery
```

"""
week_toc_prompt = PromptTemplate.from_template(week_toc_template)

week_item_toc_template = """
- You are Python Expert and Coursera Assistant.
- Give some key points in week {week_name} , chapter {week_item_name} in markdown list format.
- including project names, key concepts, etc.
- And should not be in {previous_week_items_toc} list .

for example:
```
- variables
- if / else
- expressions
- functions
```

"""
week_item_toc_prompt = PromptTemplate.from_template(week_item_toc_template)

is_concept_or_project_template = """
- Is {key_point} a concept or a project?
- Answer in one word: `concept` or `project`

for example:
- input: `Variables` , output: `concept`
- input: `Guess the number game` , output: `project`
"""
is_concept_or_project_prompt = PromptTemplate.from_template(
    is_concept_or_project_template
)

concept_slide_template = """
- You are Python Expert and Coursera Assistant.
- Give **1~3 side** notes about **{key_point} concept** in **markdown** format.
- each slide should have `h2` title
- add `---` between slides
- add detailed code snippets with comments, as detailed as possible
- add a little bit of explanation

"""
concept_slide_prompt = PromptTemplate.from_template(concept_slide_template)

project_slide_template = """
- You are Python Expert and Coursera Assistant.
- Give **2~5** side notes about **{key_point} project** in **markdown** format.
- each slide should have `h2` title
- add `---` between slides
- add detailed code snippets with comments, as detailed as possible
- add a little bit of explanation

"""
project_slide_prompt = PromptTemplate.from_template(project_slide_template)

rag_prompt = hub.pull("rlm/rag-prompt")

rag_prompt_template_without_question = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Context: {context} 
Answer:
"""
rag_prompt_without_question = PromptTemplate.from_template(
    rag_prompt_template_without_question
)


def get_rag_prompt():
    return rag_prompt


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
        | rag_prompt_without_question
        | course_toc_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_week_toc_chain(
    retriever: VectorStoreRetriever, llm: ChatOpenAI
):
    rag_chain = (
        {
            "context": retriever | _format_docs,
            
        }
        | rag_prompt_without_question
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
        | rag_prompt_without_question
        | week_item_toc_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_is_concept_or_project_chain(
    retriever: VectorStoreRetriever, llm: ChatOpenAI
):
    rag_chain = (
        {"context": retriever | _format_docs, "key_point": RunnablePassthrough()}
        | rag_prompt_without_question
        | is_concept_or_project_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_concept_slide_chain(
    retriever: VectorStoreRetriever, llm: ChatOpenAI
):
    rag_chain = (
        {"context": retriever | _format_docs, "key_point": RunnablePassthrough()}
        | rag_prompt_without_question
        | concept_slide_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_project_slide_chain(
    retriever: VectorStoreRetriever, llm: ChatOpenAI
):
    rag_chain = (
        {"context": retriever | _format_docs, "project_name": RunnablePassthrough()}
        | rag_prompt_without_question
        | project_slide_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain