## Plan: Add A Simple Gemini RAG

Build a standalone `015-simple-rag.py` lesson that follows the repository's existing root-script conventions: load `GENAI_API_KEY`, read a dedicated local `docs/` corpus, create chunks, embed documents and the user's query with Gemini, rank by cosine similarity, then provide the top chunks to `gemini-2.5-flash` for a grounded answer.

**Steps**
1. Add a small `docs/` fixture with focused Markdown or text content suitable for questions and citations. Keep the corpus intentionally small and committed as learning data.
2. Add `015-simple-rag.py` at the repository root. Reuse the client setup and error handling style from `001-basic-llm-call.py`. Implement standard-library helpers for loading files, deterministic chunking, cosine similarity, and embedding extraction. Use `gemini-embedding-001` with document/query retrieval task types, embed the corpus at startup, select the top few chunks, and call `gemini-2.5-flash` with a prompt that requires answers to use only the supplied context and say when the answer is unavailable. Print retrieved source names/scores and the final response so the retrieval and generation stages are observable.
3. Update `README.md` with the new example in the project structure, requirements/run instructions, learning path, and a short explanation of the RAG pipeline. Document that embeddings and generation both consume API quota and that indexing is performed at runtime.
4. Validate the focused script with a syntax/compile check and, when a valid `GENAI_API_KEY` is available, run a small known-answer query against the fixture. Confirm the output includes retrieved source context and a grounded answer; also test an out-of-scope question to verify the prompt's unknown-answer behavior.

**Relevant files**
- `d:/Learn/My-Projects-AI/001-basic-llm-call.py` — reuse root-level `google-genai` client initialization, `GENAI_API_KEY` lookup, and model naming conventions.
- `d:/Learn/My-Projects-AI/015-simple-rag.py` — new end-to-end RAG lesson and local retrieval implementation.
- `d:/Learn/My-Projects-AI/docs/` — new dedicated corpus fixture.
- `d:/Learn/My-Projects-AI/README.md` — document setup and execution of the new numbered example.
- `d:/Learn/My-Projects-AI/.gitignore` — inspect only if generated indexes or local artifacts are introduced; preferred design creates none.

**Verification**
1. Run `python -m py_compile .\\015-simple-rag.py` from the repository root.
2. Run `python .\\015-simple-rag.py` with a known question and verify the retrieved filenames/similarity scores and grounded answer.
3. Run an unrelated question and verify the response explicitly indicates the corpus does not contain the answer rather than inventing one.
4. Check that no API key, generated index, or unrelated file changes are included.

**Decisions**
- Use Gemini semantic embeddings, as requested, rather than keyword-only retrieval.
- Use a dedicated `docs/` folder rather than indexing arbitrary repository code; this makes the lesson predictable and avoids exposing source files to prompts.
- Build the index in memory on each run; do not add FAISS, Chroma, LangChain, or a persistent vector database for this first example.
- Keep the existing `GENAI_API_KEY` convention and root dependency set; no new package is required.
- Include source labels in the context and output, but do not promise production-grade citation guarantees.

**Further Considerations**
1. The exact embedding API response shape should be confirmed against the installed `google-genai` version while implementing; isolate that compatibility handling in one helper.
2. If API usage is unavailable during validation, compile and unit-test chunking/similarity helpers with mocked embeddings, then report the missing live check clearly.
