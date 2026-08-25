# My-Projects-AI

Small Python examples for learning how to call Google Gemini with the
`google-genai` SDK. The examples progress from a basic request to chat history,
streaming responses, personas, and multi-turn interactions.

## Requirements

- Python 3.10 or newer
- A Google Gemini API key

Install the dependencies from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install google-genai python-dotenv
```

Create a `.env` file in the repository root and add your API key:

```text
GENAI_API_KEY=your_api_key_here
```

The scripts load this value with `python-dotenv`. Do not commit `.env` or share
your API key.

## Examples

All examples use the `gemini-2.5-flash` model by default.

### 001: Basic LLM Call

Sends one prompt and prints the response.

```powershell
python .\001-basic-llm-call.py
```

### 002: Multi-Message Chat

Runs an interactive chat session that preserves conversation history. Type
`exit` to stop.

```powershell
python .\002-loop-llm-call.py
```

### 003: Streaming Response

Displays the response as Gemini generates it instead of waiting for the full
response.

```powershell
python .\003-stream-llm-call.py
```

### 004: Persona Chat

Uses a system instruction to make Gemini respond as a concise senior Python
developer mentor.

```powershell
python .\004-persona-llm.py
```

### 005: Streaming Interactions API

Uses the Interactions API and prints text delta events as they arrive.

```powershell
python ".\005-gemini-interactionsAPI-stream response.py"
```

### 006: Multi-Turn Interaction State

Demonstrates server-side interaction state by connecting related requests with
`previous_interaction_id`.

```powershell
python .\006-multi-turn-interaction.py
```

## Learning Path

1. Start with `001-basic-llm-call.py` to make a first request.
2. Use `002-loop-llm-call.py` to keep context across messages.
3. Try `003-stream-llm-call.py` to improve response feedback.
4. Customize the system instruction in `004-persona-llm.py`.
5. Compare chat sessions with the Interactions API examples.

## Notes

- Each script creates its own Gemini client and uses the API key from `.env`.
- The model ID is defined near the top of each script and can be changed.
- API calls may incur usage or quota charges according to your Google AI setup.
- These examples are intentionally simple and are not production applications.
