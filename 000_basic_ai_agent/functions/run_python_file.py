import os
import subprocess
import sys

from google.genai import types
from google.genai.types import FunctionDeclaration, Schema, Type


def _find_project_root(start_path: str):
    """Ascend directories until a pyproject.toml is found or stop at drive root."""
    current = start_path
    while True:
        if os.path.isfile(os.path.join(current, 'pyproject.toml')):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return start_path  # fallback
        current = parent

def _select_interpreter(working_dir: str):
    project_root = _find_project_root(working_dir)
    # Prefer local .venv if present
    if os.name == 'nt':
        candidate = os.path.join(project_root, '.venv', 'Scripts', 'python.exe')
    else:
        candidate = os.path.join(project_root, '.venv', 'bin', 'python')
    if os.path.isfile(candidate):
        return candidate
    # Fallback to current interpreter
    return sys.executable

def safe_write_file(working_directory: str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    # Resolve file_path relative to current working directory if not absolute
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    print(f"abs_working_dir: {abs_working_dir}")
    print(f"abs_file_path: {abs_file_path}")
    # Strict containment check: file must be inside working directory
    if not abs_file_path.startswith(abs_working_dir + os.sep):
        return ("Cannot write outside the working directory.")
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a valid file.' 
    #if file does not end in .py, return error
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a python file.'
    
    try:
        interpreter = _select_interpreter(abs_working_dir)
        final_args = [interpreter, file_path]
        final_args.extend(args)

        completed = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True
        )
        stdout = completed.stdout.decode(errors='replace')
        stderr = completed.stderr.decode(errors='replace')
        output_lines = [f"Interpreter: {interpreter}"]
        output_lines.append(f"Command: {' '.join(final_args)}")
        output_lines.append(f"Return Code: {completed.returncode}")
        output_lines.append("--- STDOUT ---")
        output_lines.append(stdout if stdout.strip() else "<no stdout>")
        output_lines.append("--- STDERR ---")
        output_lines.append(stderr if stderr.strip() else "<no stderr>")
        if completed.returncode != 0 and 'ModuleNotFoundError' in stderr:
            output_lines.append("Hint: Dependency missing in the interpreter used. Ensure 'python-dotenv' installed in the venv or project root .venv.")
        return "\n".join(output_lines)
    except subprocess.CalledProcessError as e:
        return f'Error running file "{file_path}": {e}'

# Backwards compatible alias with a clearer name for future use
def run_python_file(working_directory: str, file_path: str, args=[]):
    return safe_write_file(working_directory, file_path, args)

schema_run_python_file = FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file with the python interpreter. Accepts additional CLI args as an optional array.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "file_path": Schema(
                type=Type.STRING,
                description="The path to the file to run, relative to the working directory."
            ),
            "args": Schema(
                type=Type.ARRAY,
                items=Schema(
                    type=Type.STRING,
                    description="Additional command-line arguments to pass to the script."
                )
            ),
        }
    ),
)