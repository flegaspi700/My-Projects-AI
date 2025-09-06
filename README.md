# My-Projects-AI

## Overview
Sandbox for experimenting with:
1. A basic Google Gemini powered coding agent (function calling prototype).
2. A console calculator (with an intentionally buggy `add` implementation for testing error detection) that the agent can diagnose and propose fixes for.
3. Safe filesystem helper utilities (read, list, run, and write within a constrained working directory).

> Note: This is a learning-oriented, basic agent inspired by the freeCodeCamp tutorial/video: https://youtu.be/YtHdaXuOAks?si=0cBvFtqgibMFuPm5. Features are intentionally minimal and security-focused for educational exploration.

## Project Structure
```
000_basic_ai_agent/
	main.py                # Gemini agent entry point
	config.py              # Simple config constants
	calculator/            # Calculator mini-app
		main.py              # CLI calculator runner
		pkg/
			calculator.py      # Calculator class + expression parser
			render.py          # ASCII render helpers
	functions/             # Sandboxed helper utilities
		get_files_info.py    # List directory contents (size-aware)
		get_file_content.py  # Safe file reader
		write_file.py        # Safe writer (prevents path escape)
		run_python_file.py   # Runs Python file via project interpreter
```

## Calculator
Expression evaluation supports: `+ - * /` parentheses, unary +/- , ints & floats.

Run it:
```powershell
uv run .\calculator\main.py "2 + 3 * (4 - 1)"
```

### Intentional Bug
`Calculator.add` currently returns `a + b + 1` (on purpose). This propagates through `evaluate` because the parser routes operations through the arithmetic methods. Example:
```
2 + 2  => 5   (buggy add)
2 * 3  => 6   (multiply correct)
```
Remove the bug by editing `calculator.py` and changing `return a + b + 1` to `return a + b`.

## Gemini Agent (Prototype)
`main.py` sends the user prompt to the Gemini model. Tool/function call wiring is being iterated; current simplified version just generates text.

Run:
```powershell
uv run main.py "What is AI?"
```

Set your API key in a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

## Safe File Utilities
All helpers enforce that operations stay inside a declared working directory using `os.path.commonpath` or prefix checks. Attempts to escape (e.g. `../outside.txt`) raise errors.

## Security / Sandbox Focus
This exercise emphasizes containment and least-privilege patterns:
* Directory confinement: helper functions resolve absolute paths then verify they remain under the chosen working root (defense against `..` traversal and symlink-like relative tricks).
* Deny-by-default: operations immediately abort with an error string / exception if a path falls outside the boundary.
* Execution sandbox: `run_python_file.py` selects the project interpreter and refuses to run non-`.py` targets or paths outside the root.
* No arbitrary eval in agent tools: only whitelisted function declarations are exposed to the model (expansion requires deliberate code change).
* Calculator expression parsing: replaced `eval` with a controlled parser to avoid arbitrary code execution vectors.

Planned hardening (not yet implemented):
* Symlink resolution & explicit symlink denial.
* File descriptor / size quotas.
* Read-only mode toggle for certain operations during an agent session.
* Structured audit log of tool invocations (timestamp + arguments + outcome).
* Optional allowlist of subdirectories per operation type (read vs write vs execute).

If you extend the agent with new tools, replicate the path validation pattern before performing file I/O or code execution.

## Tests / Quick Manual Checks
Manual driver script: `test.py` in root or inside `calculator/` for calculator-specific tests. (Add formal unit tests later.)

## Environment Setup
Requires Python 3.13+ (see `pyproject.toml`). Dependencies (including `python-dotenv` and `google-genai`) are declared there.
Install with (if using uv):
```powershell
uv pip install
```
Or standard venv:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e .
```

## Future Improvements
- Toggle to enable/disable the intentional calculator bug.
- Automated pytest suite.
- Automatic execution of model function calls.
- Richer sandbox policy & logging.

## Disclaimer
Experimental code; not hardened for production. Use at your own discretion.
