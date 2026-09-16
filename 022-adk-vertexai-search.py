import os
import sys
sys.path.append("..")
import google.cloud.logging
from callback_logging import log_query_to_model, log_model_response
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.models import Gemini
from google.genai import types
from google.adk.tools import AgentTool

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)

from .tools import get_date

# Add the VertexAiSearchTool import below
from google.adk.tools import VertexAiSearchTool


load_dotenv()
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

# Create your vertexai_search_tool and update its path below
vertexai_search_tool = VertexAiSearchTool(
    search_engine_id="projects/YOUR_PROJECT_ID/locations/global/collections/default_collection/engines/YOUR_SEARCH_APP_ID"
)

vertexai_search_agent = Agent(
    name="vertexai_search_agent",
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    instruction="Use your search tool to look up facts.",
    tools=[vertexai_search_tool]
)

root_agent = Agent(
    # A unique name for the agent.
    name="root_agent",
    # The Large Language Model (LLM) that agent will use.
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    # A short description of the agent's purpose, so other agents
    # in a multi-agent system know when to call it.
    description="Answer questions using your data store access.",
    # Instructions to set the agent's behavior.
    instruction="You analyze new planet discoveries and engage with the scientific community on them.",
    # Callbacks to log the request to the agent and its response.
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    # Add the tools instructed below
    tools=[
        AgentTool(vertexai_search_agent, skip_summarization=False),
        get_date
    ]
)


####should be in a separate tools.py
from datetime import datetime, timedelta

def get_date(x_days_from_today:int):
    """
    Retrieves a date for today or a day relative to today.

    Args:
        x_days_from_today (int): how many days from today? (use 0 for today)

    Returns:
        A dict with the date in a formal writing format. For example:
        {"date": "Wednesday, May 7, 2025"}
    """

    target_date = datetime.today() + timedelta(days=x_days_from_today)
    date_string = target_date.strftime("%A, %B %d, %Y")

    return {"date": date_string}
