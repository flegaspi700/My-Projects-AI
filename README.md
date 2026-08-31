# My-Projects-AI

This repository is a learning-focused collection of Python examples built with the Google Gemini API and the `google-genai` SDK. The scripts cover the basics of making requests, maintaining chat context, streaming output, using multimodal inputs, calling tools, and creating a simple AI coding agent.

## What is in this project?

The examples progressively move from simple API calls to more advanced Gemini patterns:

- Basic single-prompt requests
- Chat sessions with memory across turns
- Streaming responses in real time
- Persona/system-instruction prompting
- Interactions API usage
- Multi-turn server-side state
- Multi-modal understanding with image and audio
- Image generation
- Tool-using interactions with Google Search
- A lightweight function-calling coding assistant

## Project structure

```text
My-Projects-AI/
├── 001-basic-llm-call.py
├── 002-loop-llm-call.py
├── 003-stream-llm-call.py
├── 004-persona-llm.py
├── 005-gemini-interactionsAPI-stream response.py
├── 006-multi-turn-interaction.py
├── 007-multimodal-understanding.py
├── 008-multimodal-generation.py
├── 009-use-tools.py
├── README.md
├── .env
├── audio/
├── images/
├── 000_basic_ai_agent/
│   ├── main.py
│   ├── call_function.py
│   ├── config.py
│   ├── pyproject.toml
│   ├── test.py
│   ├── calculator/
│   └── functions/
└── .venv/
```

## Requirements

- Python 3.10 or newer
- A Google Gemini API key
- Internet access for Gemini API calls and Google Search tool calls

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

The top-level scripts read `GENAI_API_KEY` using `python-dotenv`. The agent under the `000_basic_ai_agent` folder uses `GEMINI_API_KEY` instead, so check that file if you want to run the agent example.

> Do not commit `.env` or share your API key.

## Running the examples

All of the standalone scripts use the `gemini-2.5-flash` model by default unless they are explicitly configured otherwise.

### 001: Basic LLM call

Sends a single prompt to Gemini and prints the result.

```powershell
python .\001-basic-llm-call.py
```

### 002: Loop chat

Creates a chat session and allows multiple prompt/response turns while keeping context.

```powershell
python .\002-loop-llm-call.py
```

### 003: Streaming response

Streams the model output token by token as it arrives.

```powershell
python .\003-stream-llm-call.py
```

### 004: Persona chat

Adds a system instruction so the model responds like a senior Python mentor.

```powershell
python .\004-persona-llm.py
```

### 005: Interactions API streaming

Uses the Interactions API with a streaming response.

```powershell
python ".\005-gemini-interactionsAPI-stream response.py"
```

### 006: Multi-turn interaction state

Demonstrates passing `previous_interaction_id` so related interactions share server-side state.

```powershell
python .\006-multi-turn-interaction.py
```

### 007: Multimodal understanding

Reads an image and an audio file from the `images/` and `audio/` folders and asks Gemini to describe both.

```powershell
python .\007-multimodal-understanding.py
```

### 008: Multimodal generation

Generates an image from a text prompt and saves it into the `images/` directory.

```powershell
python .\008-multimodal-generation.py
```

### 009: Tool use with Google Search

Creates an interaction that uses the Google Search tool and prints source citations from the model output.

```powershell
python .\009-use-tools.py
```

## AI coding agent example

The project also includes a more advanced agent in the `000_basic_ai_agent` folder. It uses function declarations to allow the model to:

- list files
- read file contents
- write files
- run Python scripts

This agent is designed as a simple experiment in tool-using LLM behavior, not as a production-grade autonomous agent.

```powershell
cd .\000_basic_ai_agent
python .\main.py "List the files in the project and summarize the repo structure"
```

## Suggested learning path

1. Start with `001-basic-llm-call.py`
2. Move to `002-loop-llm-call.py` and `003-stream-llm-call.py`
3. Explore `004-persona-llm.py` and `005-gemini-interactionsAPI-stream response.py`
4. Try `006-multi-turn-interaction.py` for stateful interactions
5. Test multimodal examples in `007-multimodal-understanding.py` and `008-multimodal-generation.py`
6. Finish with tool use and the agent examples in `009-use-tools.py` and `000_basic_ai_agent/main.py`

## Notes

- These scripts are intentionally simple and educational.
- The model name is defined near the top of each script and can be changed.
- Some examples depend on local files in the `images/` and `audio/` folders.
- API usage may incur Google API charges or quota usage depending on your account and model settings.
- The project is best used for experimentation and learning rather than production deployment.
