from enum import Enum


class _BaseEnum(Enum):
    def __str__(self):
        return self.value


class VerbEnum(_BaseEnum):
    CHECK = "check"
    INFO = "info"
    LOAD = "load"
    DELETE = "delete"
    GENERATE = "generate"


class EntityEnum(_BaseEnum):
    COURSE_NAME = "course_name"


class AlgorithmEnum(_BaseEnum):
    RAG = "rag"
    SEQUENTIAL = "sequential"


class StorageEnum(_BaseEnum):
    CHROMA = "chroma"
