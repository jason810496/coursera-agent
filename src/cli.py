import argparse

from src.config import runtime_config
from src.enums import AlgorithmEnum, EntityEnum, StorageEnum, VerbEnum


def get_cli_args() -> tuple[VerbEnum, str]:
    """
    Get the command line arguments and update the runtime_config

    :return: the verb and the course_name
    """
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Coursera management commands",
    )

    # Add the settings
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="decrease output verbosity"
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="interactive mode"
    )
    parser.add_argument(
        "--algorithm",
        help="the algorithm to use",
        action="store",
        choices=[algorithm.value for algorithm in AlgorithmEnum],
        default=AlgorithmEnum.RAG.value,
    )
    parser.add_argument(
        "--storage",
        help="the storage to use",
        action="store",
        choices=[storage.value for storage in StorageEnum],
        default=StorageEnum.CHROMA.value,
    )
    parser.add_argument(
        "--skip-project",
        help="skip to check whether the key point is a project or a concept, default is True",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--exclude-file-pattern",
        help="exclude file pattern",
        action="store",
        type=str,
    )

    # Add the verbs
    verbs = parser.add_subparsers(dest="verb", required=True)

    # Add the check-config verb
    check_parser = verbs.add_parser(
        str(VerbEnum.CHECK),
        help="check current configuration",
        description="""
        Check the current configuration settings, including: 
        - course_name 
        - src_dir 
        - dist_dir 
        - chroma_host 
        - chroma_port 
        """,
    )
    check_parser.add_argument(
        str(EntityEnum.COURSE_NAME),
        help="the name of the course to check",
        action="store",
        type=str,
    )

    # Add the info verb
    info_parser = verbs.add_parser(
        str(VerbEnum.INFO),
        help="get the course information",
        description="""
        Get the course information from the src_dir
        """,
    )
    info_parser.add_argument(
        str(EntityEnum.COURSE_NAME),
        help="the name of the course to get information",
        action="store",
        type=str,
    )

    # Add the load verb
    load_parser = verbs.add_parser(
        str(VerbEnum.LOAD),
        help="Load a course, convert to OpenAI Embeddings, and store in the Chroma Vector Database",
        description="""
        1. Load the course from the src_dir
        2. Convert the course to OpenAI Embeddings
        3. Store the course embeddings in the Chroma Vector Database
        """,
    )
    load_parser.add_argument(
        str(EntityEnum.COURSE_NAME),
        help="the name of the course to load",
        action="store",
        type=str,
    )

    # Add the delete verb
    delete_parser = verbs.add_parser(
        str(VerbEnum.DELETE),
        help="delete the course from the Chroma Vector Database",
        description="""
        - prerequisite: load the course
        - delete the course from the Chroma Vector Database
        """,
    )
    delete_parser.add_argument(
        str(EntityEnum.COURSE_NAME),
        help="the name of the course to delete",
        action="store",
        type=str,
    )

    # Add the generate verb
    generate_parser = verbs.add_parser(
        str(VerbEnum.GENERATE),
        help="generate the course summary",
        description="""
        - prerequisite: load the course
        - generate the course summary in markdown format
        - store the course summary result in the dist_dir
        """,
    )
    generate_parser.add_argument(
        str(EntityEnum.COURSE_NAME),
        help="the name of the course to generate",
        action="store",
        type=str,
    )

    # Parse the arguments
    args = parser.parse_args()
    _update_runtime_config(args)
    return VerbEnum(args.verb), args.course_name


def _update_runtime_config(args):
    runtime_config.VERBOSE = args.verbose
    runtime_config.QUIET = args.quiet
    runtime_config.INTERACTIVE = args.interactive
    runtime_config.ALGORITHM = args.algorithm
    runtime_config.SKIP_PROJECT = args.skip_project
    runtime_config.EXCLUDE_PATTERN = args.exclude_file_pattern

    return args
