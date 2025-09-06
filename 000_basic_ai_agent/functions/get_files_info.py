import os
from google.genai import types
from google.genai.types import FunctionDeclaration, Schema, Type

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    # Ensure abs_directory is truly inside abs_working_dir
    if os.path.commonpath([abs_working_dir, abs_directory]) != abs_working_dir:
        return f'Error: "{directory}" is not a subdirectory of "{working_directory}".'

    def get_dir_size(path):
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total += os.path.getsize(fp)
        return total

    final_response = ""
    contents = os.listdir(abs_directory)
    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        if is_dir:
            size = get_dir_size(content_path)
        else:
            size = os.path.getsize(content_path)
        final_response += f"{'DIR ' if is_dir else 'FILE'} - {content} - {size} bytes\n"

    return final_response

schema_get_files_info = FunctionDeclaration(
    name="get_files_info",
    description="List files in a specified directory within the working directory, along with their sizes.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "directory": Schema(
                type=Type.STRING,
                description="The subdirectory to list files from (default: current directory)."
            )
        }
    ),
)