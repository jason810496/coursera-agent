from langchain import hub
from langchain_core.prompts import PromptTemplate

from src.config import coursera_config


def _get_prompt_template(prompt_name: str) -> str:
    return open(f"{coursera_config.PROMPTS_FOLDER}/{prompt_name}.txt").read()


course_toc_template = _get_prompt_template("course_toc_prompt")
course_toc_prompt = PromptTemplate.from_template(course_toc_template)

week_toc_template = _get_prompt_template("week_toc_prompt")
week_toc_prompt = PromptTemplate.from_template(week_toc_template)

week_item_toc_template = _get_prompt_template("week_item_toc_prompt")
week_item_toc_prompt = PromptTemplate.from_template(week_item_toc_template)

is_concept_or_project_template = _get_prompt_template("is_concept_or_project_prompt")
is_concept_or_project_prompt = PromptTemplate.from_template(
    is_concept_or_project_template
)

concept_slide_template = _get_prompt_template("concept_slide_prompt")
concept_slide_prompt = PromptTemplate.from_template(concept_slide_template)

project_slide_template = _get_prompt_template("project_slide_prompt")
project_slide_prompt = PromptTemplate.from_template(project_slide_template)

rag_prompt = hub.pull("rlm/rag-prompt")

rag_without_question_prompt = PromptTemplate.from_template(
    """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Context: {context} 
Answer:
"""
)
