import asyncio
import os
from typing import TYPE_CHECKING

from src.algorithm import BaseAlgorithm
from src.log import rich_print
from src.utils import parse_markdown_list


from src.config import runtime_config
from src.schema import (
    Course,
    CourseResult,
    CourseWeekResult,
    CourseWeekItemResult,
    KeyPoint,
)

from src.rag.core import save_file, get_retriever, get_llm
from src.rag.chain import (
    get_rag_chain,
)
from src.rag.prompts import (
    course_toc_template,
    week_toc_template,
    week_item_toc_template,
    is_concept_or_project_template,
    concept_slide_template,
    project_slide_template,
)
from src.rag.vector_database import delete_collection

if TYPE_CHECKING:
    from langchain_openai import ChatOpenAI
    from langchain_core.vectorstores import VectorStoreRetriever
    from langchain_core.runnables import RunnablePassthrough


class RAGAlgorithm(BaseAlgorithm):
    # set up configuration
    course_name: str | None = None
    collection_name: str | None = None
    # set up RAG chain
    retriever: "VectorStoreRetriever" | None = None
    llm: "ChatOpenAI" | None = None
    rag_chain: "RunnablePassthrough" | None = None

    def __init__(
        self,
        course_source: Course,
        dist_dir: str,
        final_file_path: str,
    ) -> None:
        super().__init__(course_source, dist_dir, final_file_path)
        self.course_name = course_source.name
        self.collection_name = course_source.name
        # internal variables
        self.course_toc_resp = ""
        self.course_toc = []
        self.week_toc_resp = ""
        self.week_toc = []
        self.week_item_toc_resp = ""
        self.week_item_toc = []
        # prevent duplicate entries
        self.previous_week_toc = []
        self.previous_week_item_toc = []
        self.previous_key_point = []

    # private methods for `summarize_course`
    def _init_rag_chain(self):
        self.retriever = get_retriever(self.collection_name)
        self.llm = get_llm()
        self.rag_chain = get_rag_chain(self.retriever, self.llm)
        if runtime_config.VERBOSE:
            self.logger.debug("RAG chain initialized")
            self.logger.debug(self.rag_chain)
            self.logger.debug(self.retriever)
            self.logger.debug(self.llm)

    def load_course(self) -> None:
        self._init_rag_chain()

    async def _store_course_concurrently(self, course: Course):
        # private methods for `store_course`
        async def store_course(file_path: str):
            self.logger.debug(f"Storing {file_path}")
            save_file(self.collection_name, file_path)

        tasks = []
        for week in course.weeks:
            for week_item in week.items:
                for item in week_item.items:
                    tasks.append(store_course(item.path))

        rich_print(f"Storing [bold]{course.name}[/bold] to vector database")

        await asyncio.gather(*tasks)

    def delete_course(self) -> None:
        delete_collection(self.collection_name)
        rich_print(f"Deleted [bold]{self.collection_name}[/bold] collection")

    def _generate_course(self) -> CourseResult:
        self._init_rag_chain()
        # get course table of content
        self.course_toc_resp: str = self.rag_chain.invoke(course_toc_template)
        if runtime_config.VERBOSE:
            self.logger.debug("Course Table of Content")
            self.logger.debug(self.course_toc_resp)
        self.course_toc: list = parse_markdown_list(self.course_toc_resp)
        self.logger.debug("Course Table of Content")
        self.logger.debug(self.course_toc_resp)

        rich_print("[bold]Generating course TOC[/bold]")
        rich_print(self.course_toc)

        # Processing Weeks
        self.course_result = CourseResult(
            name=self.course_name,
            toc=self.course_toc_resp,
            weeks=[self._generate_week(week_name) for week_name in self.course_toc],
        )

    def _generate_week(self, week_name: str) -> CourseWeekResult:
        # prevent duplicate entries
        self.previous_week_toc.append(week_name)
        self.logger.debug("previous_week_toc")
        self.logger.debug(self.previous_week_toc)

        week_toc_response = self.rag_chain.invoke(
            week_toc_template.format(
                week_name=week_name, previous_weeks_toc=str(self.previous_week_item_toc)
            )
        )
        cur_week_toc = parse_markdown_list(week_toc_response)
        self.logger.debug(cur_week_toc)

        rich_print(
            f"[bold]Generating week items for [green]{week_name}[/green] week [/bold]"
        )
        rich_print(cur_week_toc)

        return CourseWeekResult(
            name=week_name,
            toc=week_name,
            items=[
                self._generate_week_item(week_item_name)
                for week_item_name in cur_week_toc
            ],
        )

    def _generate_week_item(self, week_item_name: str) -> CourseWeekItemResult:
        # prevent duplicate entries
        self.previous_week_item_toc.append(week_item_name)
        self.logger.debug("previous_week_item_toc")
        self.logger.debug(self.previous_week_item_toc)

        week_item_toc = self.rag_chain.invoke(
            week_item_toc_template.format(
                week_name=self.previous_week_toc[-1],
                week_item_name=week_item_name,
                previous_week_items_toc=str(self.previous_key_point),
            )
        )
        cur_week_item_toc = parse_markdown_list(week_item_toc)
        self.logger.debug(cur_week_item_toc)

        rich_print(
            f"[bold]Generating key points for [green]{week_item_name}[/green] week item[/bold]"
        )
        rich_print(cur_week_item_toc)

        return CourseWeekItemResult(
            name=week_item_name,
            toc=week_item_name,
            items=[
                self._generate_course_file(key_point) for key_point in cur_week_item_toc
            ],
        )

    def _generate_course_file(self, key_point: str) -> KeyPoint:
        # prevent duplicate entries
        self.previous_key_point.append(key_point)
        key_point_type = "concept"

        if not runtime_config.SKIP_PROJECT:
            # runtime_config.SKIP_PROJECT
            # ignore checking if key point is a concept or project
            # generate only concept slides
            key_point_type = self._is_concept_or_project(key_point)

        final_path = f"{self.dist_dir}/{key_point}.md"
        self.logger.debug(f"final_path: {final_path}")

        rich_print(f"Generating slides for {key_point}...")

        if key_point_type == "concept":
            self._generate_concept_slide(key_point, final_path)
        else:
            self._generate_project_slide(key_point, final_path)

        return KeyPoint(name=key_point, path=final_path, type=key_point_type)

    def _is_concept_or_project(self, key_point: str) -> str:
        """
        determine if a key point is a `concept` or a `project`
        """
        is_concept_or_project = self.rag_chain.invoke(
            is_concept_or_project_template.format(key_point=key_point)
        )
        self.logger.debug(f"{key_point} is {is_concept_or_project}")
        return is_concept_or_project

    def _generate_concept_slide(self, key_point: str, final_path: str) -> str:
        concept_slide = self.rag_chain.invoke(
            concept_slide_template.format(key_point=key_point)
        )
        self.logger.debug(f"{key_point} slide:\n{concept_slide}")
        self._write_resp_to_file(concept_slide, final_path)

    def _generate_project_slide(self, key_point: str, final_path: str) -> str:
        project_slide = self.rag_chain.invoke(
            project_slide_template.format(key_point=key_point)
        )
        self.logger.debug(f"{key_point} slide:\n{project_slide}")
        self._write_resp_to_file(project_slide, final_path)

    def _aggregate_course(self):
        rich_print("Aggregating course slides...")
        # check if dist_dir exists
        if not os.path.exists(self.dist_dir):
            os.makedirs(self.dist_dir, exist_ok=True)
        # concat all slides
        with open(self.final_file_path, "w") as final_file:
            # add slide title
            final_file.write(f"# {self.course_name}\n\n---\n\n")
            # add week items
            for week in self.course_result.weeks:
                # add week_name and table of content
                final_file.write(f"# {week.name}\n\n---\n\n")
                final_file.write(week.toc)
                final_file.write("\n---\n\n")

                for week_item in week.items:
                    # add week_item_name and table of content
                    final_file.write(f"## {week_item.name}\n\n---\n\n")
                    final_file.write(week_item.toc)
                    final_file.write("\n---\n\n")

                    for key_point in week_item.items:
                        with open(key_point.path, "r") as key_point_file:
                            final_file.write(key_point_file.read())
                            final_file.write("\n\n")
