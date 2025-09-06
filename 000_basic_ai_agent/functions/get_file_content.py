import os
from config import MAX_CHARS
from google.genai import types
from google.genai.types import FunctionDeclaration, Schema, Type

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Ensure abs_file_path is truly inside abs_working_dir
    if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
        return f'Error: "{file_path}" is not a subdirectory of "{working_directory}".'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a valid file.'
    
    file_content_string = ""
    try:
        with open(abs_file_path, 'r') as file:
            file_content_string = file.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += f'[... FILE "{file_path}" TRUNCATED TO {MAX_CHARS} CHARACTERS ...]'

        return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {str(e)}'

schema_get_file_content = FunctionDeclaration(
    name="get_file_content",
    description="Retrieve the content of a specified file as a string constrained within the working directory.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "file_path": Schema(
                type=Type.STRING,
                description="The path to the file to retrieve content from."
            )
        }
    ),
)