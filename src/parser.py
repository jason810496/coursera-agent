'''
get file path and load to schema
'''
import os 

from .schema import (
    Course,
    CourseWeek,
    CourseWeekItem,
    CourseSubtitleFile,
)
from .config import coursera_config

def _get_course_subtitle_files(path:str) -> list[CourseSubtitleFile]:
    '''
    get all srt files in path
    '''
    return [
        CourseSubtitleFile(
            name=f.name,
            path=f.path
        )
        for f in os.scandir(path)
        if f.name.endswith('.srt')
    ]

def _get_course_html_files(path:str) -> list[CourseSubtitleFile]:
    '''
    get all html files in path
    '''
    return [
        CourseSubtitleFile(
            name=f.name,
            path=f.path
        )
        for f in os.scandir(path)
        if f.name.endswith('.html')
    ]

def _get_course_week_items(path:str) -> list[CourseWeekItem]:
    '''
    get all week items in path
    '''
    return [
        CourseWeekItem(
            name=f.name,
            path=f.path,
            items=_get_course_subtitle_files(f.path) + _get_course_html_files(f.path)
        )
        for f in os.scandir(path)
        if f.is_dir()
    ]


def _get_course_weeks(path:str) -> list[CourseWeek]:
    '''
    get all weeks in path
    '''
    # check if week is exclude
    exclude_list = coursera_config.EXCLUDE_WEEKS
    valid_weeks = [
        f
        for f in os.scandir(path)
        if f.is_dir() and f.name not in exclude_list
    ]
    return [
        CourseWeek(
            name=f.name,
            path=f.path,
            items=_get_course_week_items(f.path)
        )
        for f in valid_weeks
    ]

def get_course(path:str) -> Course:
    '''
    get course from path
    '''
    # check if course path exists
    if not os.path.exists(path):
        raise FileNotFoundError(f'Course path not found: {path}')

    return Course(
        name=os.path.basename(path),
        path=path,
        weeks=_get_course_weeks(path)
    )