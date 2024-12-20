import time
import importlib

from src.config import coursera_config, chroma_config, langchain_config, runtime_config
from src.parser import get_course as parser_get_course
from src.log import rich_print, get_logger
from src.algorithm import BaseAlgorithm
from src.enums import AlgorithmEnum
from src.schema import Course, CourseResult


class CourseAgent:
    algorithm_map = {
        AlgorithmEnum.RAG.value: ("src.rag.algorithm", "RAGAlgorithm"),
        AlgorithmEnum.SEQUENTIAL.value: (
            "src.sequential.algorithm",
            "SequentialAlgorithm",
        ),
    }
    algorithm: BaseAlgorithm | None = None

    def __init__(self, course_name: str):
        # set up configuration
        self.course_name = course_name
        self.course_source = CourseAgent.get_course_info(course_name)
        self.timestamp = f"{course_name}-{time.strftime('%Y-%m-%d-%H-%M-%S')}"
        self.src_dir = f"{coursera_config.INPUT_ROOT_FOLDER}/{self.course_name}"
        self.dist_dir = f"{coursera_config.RESULT_ROOT_FOLDER}/{self.timestamp}"
        self.final_file_path = f"{self.dist_dir}/final-{self.timestamp}.md"
        self.logger = get_logger()
        # load module dynamically
        module = importlib.import_module(
            self.algorithm_map[runtime_config.ALGORITHM][0]
        )
        class_: BaseAlgorithm = getattr(
            module, self.algorithm_map[runtime_config.ALGORITHM][1]
        )
        self.algorithm = class_(
            course_source=self.course_source,
            dist_dir=self.dist_dir,
            final_file_path=self.final_file_path,
        )

    @staticmethod
    def check_config():
        logger = get_logger()
        logger.info("Current configuration:")
        logger.info("CourseAgent:")
        rich_print(coursera_config)
        logger.info("Chroma:")
        rich_print(chroma_config)
        logger.info("Langchain:")
        rich_print(langchain_config)

    @staticmethod
    def get_course_info(course_name: str) -> Course:
        return parser_get_course(f"{coursera_config.INPUT_ROOT_FOLDER}/{course_name}")

    def load_course(self):
        self.algorithm.load_course()

    def delete_course(self):
        self.algorithm.delete_course()

    def summarize_course(self):
        self.algorithm.summarize_course()

    def get_summarize_course_result(self) -> CourseResult:
        return self.algorithm.get_summarize_course_result()
