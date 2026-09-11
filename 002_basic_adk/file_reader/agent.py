"""
File Reader Assistant Agent
Demonstrates MCP tools integration with ADK using the filesystem MCP server.
Reference: https://google.github.io/adk-docs/tools-custom/mcp-tools/
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Define the folder to allow file access (must be absolute path)
ALLOWED_PATH = os.path.abspath("./my_files")

# Create the folder if it doesn't exist
os.makedirs(ALLOWED_PATH, exist_ok=True)
#print(ALLOWED_PATH)

root_agent = LlmAgent(
    model='gemini-3.5-flash',
    name='file_reader_assistant',
    description='Helps users read and explore files using MCP tools.',
    instruction='Help the user manage their files. You can list files, read files, etc.',
    tools=[
     McpToolset(
      connection_params=StdioConnectionParams(
       server_params=StdioServerParameters(
        command='npx',
        args=['-y',
              '@modelcontextprotocol/server-filesystem',
              ALLOWED_PATH,
              ],
            ),
        ),
        # Filter to only expose safe, read-only tools
        tool_filter=['list_directory', 'read_file'],
    )
    ],
)

