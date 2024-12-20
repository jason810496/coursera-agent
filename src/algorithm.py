from abc import ABC, abstractmethod
import os

from src.schema import (
    Course,
    CourseResult,
    CourseWeek,
    CourseWeekItem,
    CourseFile,
    CourseWeekResult,
    CourseWeekItemResult,
    KeyPoint,
)
from src.log import get_logger, rich_print


class BaseAlgorithm(ABC):
    course_source: Course | None = None
    course_result: CourseResult | None = None
    dist_dir: str | None = None
    final_file_path: str | None = None
    logger = get_logger()

    def __init__(
        self, course_source: Course, dist_dir: str, final_file_path: str
    ) -> None:
        self.course_source = course_source
        self.dist_dir = dist_dir
        self.final_file_path = final_file_path

    def summarize_course(self):
        """
        Summarize the course and store the result in `course_result`
        """
        self._generate_course()
        self._aggregate_course()

    def get_summarize_course_result(self) -> CourseResult:
        return self.course_result

    @abstractmethod
    def load_course(self) -> None:
        pass

    @abstractmethod
    def delete_course(self) -> None:
        pass

    @abstractmethod
    def _generate_course(self) -> None:
        pass

    @abstractmethod
    def _generate_course_file(self, course_file: CourseFile) -> KeyPoint:
        pass

    def _generate_course(self):
        self.course_result = CourseResult(
            name=self.course_source.name,
            toc=None,
            weeks=[
                self._generate_week(course_week)
                for course_week in self.course_source.weeks
            ],
        )

    def _generate_week(self, course_week: CourseWeek) -> CourseWeekResult:
        return CourseWeekResult(
            name=course_week.name,
            toc=None,
            items=[
                self._generate_week_item(course_week_item)
                for course_week_item in course_week.items
            ],
        )

    def _generate_week_item(
        self, course_week_item: CourseWeekItem
    ) -> CourseWeekItemResult:
        return CourseWeekItemResult(
            name=course_week_item.name,
            toc=None,
            items=[
                self._generate_course_file(course_file)
                for course_file in course_week_item.items
            ],
        )

    def _aggregate_course(self):
        rich_print("Aggregating course slides...")
        # check if dist_dir exists
        if not os.path.exists(self.dist_dir):
            os.makedirs(self.dist_dir, exist_ok=True)
        # concat all slides
        with open(self.final_file_path, "w") as final_file:
            # add slide title
            final_file.write(f"# {self.course_source.name}\n\n---\n\n")
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

    def _write_result_to_file(self, result: str, file_path: str):
        # parse folder and filename
        folder_path = os.path.dirname(file_path)
        # create folder if not exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        # write to file
        self.logger.debug(f"Writing to {file_path}")
        with open(file_path, "w") as f:
            f.write(result)
