"""
Name Extractor - Demonstrates Session State Basics
Shows how to use output_key to save data and access it via session.state.

Reference: https://google.github.io/adk-docs/sessions/state.md
"""
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='name_extractor',
    instruction='Extract the person\'s name from the message. Return ONLY the name, nothing else.',
    output_key='user_name',
)
