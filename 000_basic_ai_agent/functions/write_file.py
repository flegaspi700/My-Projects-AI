# Safely write a file, ensuring it is inside the working directory and allowing new subdirectories
import os
from google.genai import types
from google.genai.types import FunctionDeclaration, Schema, Type

def safe_write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    # Resolve file_path relative to current working directory if not absolute
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    print(f"abs_working_dir: {abs_working_dir}")
    print(f"abs_file_path: {abs_file_path}")
    # Strict containment check: file must be inside working directory
    if not abs_file_path.startswith(abs_working_dir + os.sep):
        return ("Cannot write outside the working directory.")
    # Create subdirectories if they don't exist
    os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    try:
        with open(abs_file_path, 'w') as file:
            file.write(content)
        print(f"File updated: {abs_file_path}")
        return f'Success: Content written to "{file_path}".'
    except Exception as e:
        return f'Error writing to file "{file_path}": {str(e)}'

schema_safe_write_file = FunctionDeclaration(
    name="safe_write_file",
    description="Overwrite or writes content to a specified file within the working directory.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "file_path": Schema(
                type=Type.STRING,
                description="The path to the file to write to, relative to the working directory."
            ),
            "content": Schema(
                type=Type.STRING,
                description="The content to write to the file."
            )
        }
    ),
)