from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser


from src.algorithm import BaseAlgorithm
from src.rag.core import get_llm
from src.log import rich_print

from src.schema import (
    Course,
    CourseFile,
    KeyPoint,
)


class SequentialAlgorithm(BaseAlgorithm):
    slide_template_prompt: ChatPromptTemplate | None = None
    llm: ChatOpenAI | None = None
    chain: RunnablePassthrough | None = None

    def __init__(
        self, course_source: Course, dist_dir: str, final_file_path: str
    ) -> None:
        super().__init__(course_source, dist_dir, final_file_path)
        self.slide_template_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        "You are Coursera Assistant that excels in summarizing course note into markdown."
                    )
                ),
                HumanMessagePromptTemplate.from_template("{text}"),
            ]
        )
        self.llm = get_llm()
        self.chain = self.slide_template_prompt | self.llm | StrOutputParser()

    def load_course(self) -> None:
        rich_print("[red]Sequential algorithm does not support loading courses [/red]")

    def delete_course(self) -> None:
        rich_print("[red]Sequential algorithm does not support deleting courses [/red]")

    def _generate_course_file(self, course_file: CourseFile) -> KeyPoint:
        file_content = open(course_file.path, "r").read()
        rich_print(f"Generating slides for {course_file.path}...")
        try:
            result = self.chain.invoke({"text": file_content})
        except Exception as e:
            rich_print(f"[red]Error during generation: {e}[/red]")
            return KeyPoint(
                name=course_file.path,
                path=course_file.path,
                type="error",
            )
        rich_print(f"Generated result: {result}")
        # get the file name
        file_name = course_file.path.split("/")[-1]
        # replace the file extension with .md
        file_name = file_name.split(".")[0] + ".md"
        final_path = f"{self.dist_dir}/{file_name}"
        self.logger.debug(f"Writing to {final_path}")
        self._write_result_to_file(result, final_path)

        return KeyPoint(
            name=file_name,
            path=final_path,
            type="concept",
        )
