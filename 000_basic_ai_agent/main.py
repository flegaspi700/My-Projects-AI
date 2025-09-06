import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_safe_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function

def main():

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    #Google Gen AI SDK Documentation: https://googleapis.github.io/python-genai/

    # Validate API key early
    if not api_key:
        print("Error: GEMINI_API_KEY not set in environment (.env).")
        sys.exit(1)

    system_prompt = (
        """You are a helpful coding agent.
        When a use asks a question or makes a request, make a function call plan. You can perform the following operation: 
        
        -list files and directories
        -read file content
        -write to a file
        -run a python file with the python interpreter
        
        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
        )

    verbose_flag = False

    #get input from user
    if len(sys.argv) < 2:
        print("Usage: python main.py <your question>")
        sys.exit(1)
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    messages = [
        types.Content(role='user', parts=[types.Part(text=prompt)])
    ]

    # Define tool with correct field name expected by SDK
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_safe_write_file,
            schema_run_python_file
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
        #max_output_tokens=1024,
    )

    max_iter = 20

    for i in range(0, max_iter):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config
        )

        if response is None or response.usage_metadata is None:
            print("No usage metadata available.")
            return

        if verbose_flag:
            print(f"Model Version: {response.model_version}")
            print(f"User Message: {prompt}")
            print(f"Assistant Message: {response.text}")
            print(f"prompt Tokens Used: {response.usage_metadata.prompt_token_count}")
            print(f"Response Tokens Used: {response.usage_metadata.candidates_token_count}")
            #print(f"Total Tokens Used: {response.response_metadata['token_usage']['total_tokens']}")

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                # SDK exposes 'args'; older docs may mention 'arguments'
                fc_args = getattr(function_call_part, 'args', None)
                if fc_args is None:
                    fc_args = getattr(function_call_part, 'arguments', None)
                result = call_function(function_call_part, verbose=verbose_flag)
                #print(f"Function Call Result: {result}")
                # Now, send the function call result back to the model for final response
                messages.append(result)
        else:
            #final agent message
            print(response.text)
            return


main()