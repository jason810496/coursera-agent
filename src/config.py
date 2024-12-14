from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class CourseraConfig(BaseSettings):
    INPUT_ROOT_FOLDER:str = Field(default='.')
    EXCLUDE_WEEKS:list = Field(default=[])
    RESULT_ROOT_FOLDER:str = Field(default='.')

    model_config = SettingsConfigDict(
        env_prefix='COURSERA_',
    )
    

coursera_config = CourseraConfig()

class LangChainConfig(BaseSettings):
    CHUNK_SIZE:int = Field(default=200)
    CHUNK_OVERLAP:int = Field(default=30)
    ADD_START_INDEX:bool = Field(default=True)
    API_KEY:Optional[str] = Field(default=None)
    TRACING_V2:Optional[bool] = Field(default=None)

    model_config = SettingsConfigDict(
        env_prefix='LANGCHAIN_',
    )

langchain_config = LangChainConfig()

class ChromaConfig(BaseSettings):
    HOST:str = Field(default='127.0.0.1')
    PORT:int = Field(default=8888)

    model_config = SettingsConfigDict(
        env_prefix='CHROMA_',
    )

chroma_config = ChromaConfig()

class RuntimeConfig(BaseSettings):
    VERBOSE:bool = Field(default=False)
    QUIET:bool = Field(default=False)
    INTERACTIVE:bool = Field(default=False)

runtime_config = RuntimeConfig()