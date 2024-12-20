"""
get file path and load to schema
"""

import os
import re

from src.schema import (
    Course,
    CourseWeek,
    CourseWeekItem,
    CourseFile,
)
from src.config import coursera_config, runtime_config
from src.log import get_logger

logger = get_logger()


def _get_course_files(path: str) -> list[CourseFile]:
    """
    get all files in path
    """
    course_files = []
    for f in os.scandir(path):
        if f.is_dir():
            course_files.extend(_get_course_files(f.path))
        else:
            if not (f.name.endswith(".html") or f.name.endswith(".srt")):
                logger.debug(f"Skipping file: {f.name}")
                continue
            # check exclude pattern
            logger.debug(f"Checking file: {f.name}")
            if (
                runtime_config.EXCLUDE_PATTERN is not None
                and re.search(runtime_config.EXCLUDE_PATTERN, f.name) is not None
            ):
                logger.debug(f"Skipping file: {f.name}")
                continue
            course_files.append(CourseFile(name=f.name, path=f.path))

    return course_files


def _get_course_week_items(path: str) -> list[CourseWeekItem]:
    """
    get all week items in path
    """
    return [
        CourseWeekItem(
            name=f.name,
            path=f.path,
            items=_get_course_files(f.path),
        )
        for f in os.scandir(path)
        if f.is_dir()
    ]


def _get_course_weeks(path: str) -> list[CourseWeek]:
    """
    get all weeks in path
    """
    # check if week is exclude
    exclude_list = coursera_config.EXCLUDE_WEEKS
    valid_weeks = [
        f for f in os.scandir(path) if f.is_dir() and f.name not in exclude_list
    ]
    return [
        CourseWeek(name=f.name, path=f.path, items=_get_course_week_items(f.path))
        for f in valid_weeks
    ]


def get_course(path: str) -> Course:
    """
    get course from path
    """
    # check if course path exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Course path not found: {path}")

    return Course(name=os.path.basename(path), path=path, weeks=_get_course_weeks(path))
