'''
logger setup , import logger instance in other modules
'''

import logging
import sys
from rich import print as rich_print
from rich.tree import Tree
from rich.text import Text

from src.config import runtime_config , coursera_config
from src.schema import (
    Course,
    CourseResult
)

logger = None

class CustomFormatter(logging.Formatter):
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    LEVEL_FORMAT = '%(levelname)s'
    MESSAGE_FORMAT = '%(message)s'

    COLORS = {
        logging.DEBUG: BLUE ,
        logging.INFO: GREEN ,
        logging.WARNING: YELLOW ,
        logging.ERROR: RED ,
        logging.CRITICAL: RED ,
    }

    def format(self, record):
        log_fmt = f"[{self.COLORS[record.levelno]}{self.LEVEL_FORMAT}{self.END}] {self.MESSAGE_FORMAT}"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger():
    if runtime_config.VERBOSE:
        logger.setLevel(logging.DEBUG)

    if runtime_config.VERBOSE:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(CustomFormatter())

        logger.addHandler(ch)

def get_logger():
    global logger
    if logger is None:
        logger = logging.getLogger("coursera-agent")
        setup_logger()

    return logger

def print_course_tree(course:Course):
    tree = Tree(
        f":open_file_folder: [link file://{coursera_config.ROOT_FOLDER}/{course.name}]{course.name}",
        # f"{course.name}",
        guide_style="dark_blue",
    )
    for week in course.weeks:
        week_tree = tree.add(
            # f":open_file_folder: [link file://{week.path}]{week.name}",
            f"{week.name}",
            guide_style="blue3"
        )
        for week_item in week.items:
            week_item_tree = week_tree.add(
                # f":open_file_folder: [link file://{week_item.path}]{week_item.name}",
                f"{week_item.name}",
                guide_style="deep_sky_blue1"
            )
            for item in week_item.items:
                week_item_tree.add(
                    # f":open_file_folder: [link file://{item.path}]{item.name}",
                    f"[link file://{item.path}]{item.name}",
                    guide_style="cyan1"
                )

    rich_print(tree)

def print_course_result_tree(course_result:CourseResult):
    tree = Tree(course_result.name)
    for week in course_result.weeks:
        week_tree = tree.add(week.name)
        for week_item in week.items:
            week_item_tree = week_tree.add(week_item.name)
            for item in week_item.items:
                week_item_tree.add(item.name)

    rich_print(tree)