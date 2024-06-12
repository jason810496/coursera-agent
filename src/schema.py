from pydantic import BaseModel, Field


# schema for store metadata reading from course directory
class CourseSubtitleFile(BaseModel):
    name:str = Field(examples="01_introduction.en.srt")
    path:str = Field(examples="/path/to/interactive-python-1/01_week-0-statements-expressions-variables/01_week-0a-expressions/01_introduction.en.srt")

class CourseWeekItem(BaseModel):
    name:str = Field(examples="01_week-0a-expressions")
    path:str = Field(examples="/path/to/interactive-python-1/01_week-0-statements-expressions-variables/01_week-0a-expressions")
    items:list[CourseSubtitleFile] = Field(min_length=0) # allow empty list

class CourseWeek(BaseModel):
    name:str = Field(examples="01_week-0-statements-expressions-variables")
    path:str = Field(examples="/path/to/interactive-python-1/01_week-0-statements-expressions-variables")
    items:list[CourseWeekItem] = Field(min_length=0) # allow empty list

class Course(BaseModel):
    name:str = Field(examples="interactive-python-1")
    path:str = Field(examples="/path/to/interactive-python-1")
    weeks:list[CourseWeek] = Field(min_length=0) # allow empty list

# schema for store tree structure of generated course summary

class KeyPoint(BaseModel):
    name:str = Field(examples="variables")
    path:str = Field(examples="/path/to/interactive-python-1/01_week-0-statements-expressions-variables/01_week-0a-expressions/variables")
    type:str = Field(examples="concept")

class CourseWeekItemResult(BaseModel):
    name:str = Field(examples="01_week-0a-expressions")
    toc:str = Field(examples="01_week-0a-expressions")
    items:list[KeyPoint] = Field(min_length=0) # allow empty list

class CourseWeekResult(BaseModel):
    name:str = Field(examples="01_week-0-statements-expressions-variables")
    toc:str = Field(examples="01_week-0-statements-expressions-variables")
    items:list[CourseWeekItemResult] = Field(min_length=0) # allow empty list

class CourseResult(BaseModel):
    name:str = Field(examples="interactive-python-1")
    toc:str = Field(examples="01_week-0-statements-expressions-variables")
    weeks:list[CourseWeekResult] = Field(min_length=0) # allow empty list