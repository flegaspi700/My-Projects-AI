import os
from google import genai
from dotenv import load_dotenv

#load environment variables 
load_dotenv()

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set in environment variables")

#initialize the client
client = genai.Client(api_key=api_key)

# Define a custom agent based from the managed agent "antigravity-preview-05-2026"
base_agent_id = "antigravity-preview-05-2026"
model = "gemini-2.5-flash"
agent_id = "my-custom-agent-03"

# Try to create it; if it already exists, fetch it instead
try:
    agent = client.agents.create(
        id=agent_id,
        base_agent=base_agent_id,
        agent_config={"type": "antigravity", "model": model},
        system_instruction="You are a math analysis agent. Generate sequences, visualize them.",
        base_environment={
            "type": "remote",
            "sources": [{
                "type": "inline",
                "target": ".agents/AGENTS.md",
                "content": "Always include a chart and a summary table in your reports.",
            }],
        },
    )
    print(f"Created new agent: {agent.id}")
except Exception as e:
    if "already exists" in str(e):
        agent = client.agents.get(id=agent_id)
        print(f"Loaded existing agent: {agent.id}")
    else:
        raise e

# call the agent to verify it works
result = client.interactions.create(
    agent=agent_id,
    input="Generate the first 50 prime numbers, plot their distribution",
    environment="remote",
)

print(result.output_text)