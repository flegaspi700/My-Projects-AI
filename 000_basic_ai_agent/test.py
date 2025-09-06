from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import safe_write_file
from functions.run_python_file import safe_write_file as run_python_file

def main():
    working_directory = "calculator"  # Change this to your desired working directory   
    print(run_python_file(working_directory, "main.py", ["2 + 2"]))
    # print(get_file_content(working_directory, "lorem.txt"))
    #print(safe_write_file(working_directory, "lorem.txt", "MY Newest test content."))
    #print(safe_write_file(working_directory, "pkg/newfile.txt", "This is another test content in a subdirectory."))
    #print(safe_write_file(working_directory, "../outside.txt", "This should fail."))  # This should fail

main()