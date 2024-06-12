import asyncio
import os 
import shutil
import time
import argparse
import textwrap
import subprocess

from src.service import CourseAgent
from src.log import rich_print , print_course_tree , print_course_result_tree
from src.cli import get_cli_args

if __name__ == '__main__':
    args = get_cli_args()

    verb = args.verb
    course_name = args.course_name
    coursera_agent = CourseAgent(course_name=course_name)


    if verb == "check":
        rich_print(f"Checking configuration for course: [bold]{course_name}")
        coursera_agent.check_config()
    elif verb == "info":
        course = coursera_agent.get_course_info()
        print_course_tree(course)
    elif verb == "load":
        rich_print(f"Loading course: [bold]{course_name}")
        coursera_agent.load_course()
    elif verb == "delete":
        rich_print(f"Deleting course: [bold]{course_name}")
        coursera_agent.delete_course()
    elif verb == "generate":
        rich_print(f"Generating course summary: [bold]{course_name}")
        coursera_agent.summarize_course()
        course_result = coursera_agent.get_summarize_course_result()
        rich_print(f"[bold][green]Finished generating {course_name} summary[/bold][/green]\n")
        print_course_result_tree(course_result)
        rich_print(f"Summary stored at: [bold]{coursera_agent.final_file_path}")
        # copy final file and open subprocess to turn it into pdf
        copy_path = str(coursera_agent.final_file_path)
        copy_path = copy_path.replace(".md","-copy.md")
        shutil.copy(coursera_agent.final_file_path,copy_path)
        rich_print(f"Summary copied at: [bold]{copy_path}[/bold]")
        marp_result =  subprocess.Popen(f"marp {copy_path} --pdf",stdout=subprocess.PIPE,shell=True)
        marp_result.wait()
        rich_print(marp_result.stdout.read().decode("utf-8"))

        rich_print(f"PDF stored at: [bold]{copy_path.replace('.md','.pdf')}[/bold]")