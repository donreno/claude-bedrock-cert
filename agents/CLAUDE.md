# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup (uses uv, not pip/venv directly)
uv venv
source .venv/bin/activate
uv pip install -e .

# Run the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file / test
uv run pytest tests/test_document.py
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

## Architecture

This is an MCP (Model Context Protocol) server exposing document-processing tools to AI assistants.

- `main.py` creates the `FastMCP` server instance (`mcp = FastMCP("docs")`) and registers tools onto it with `mcp.tool()(function_name)`. This is the wiring point — a tool implemented in `tools/` has no effect on the running server until it's registered here.
- `tools/` contains the actual tool implementations as plain Python functions (not classes). Each function is independently unit-testable without any MCP machinery. Currently: `tools/math.py` (`add`) and `tools/document.py` (`binary_document_to_markdown`, built on `markitdown` to convert DOCX/PDF binary data to markdown text).
- `tests/` mirrors `tools/` (e.g. `tests/test_document.py` tests `tools/document.py`) and uses fixtures under `tests/fixtures/` for binary file conversion tests.

### Adding a new tool

1. Write the function in the relevant module under `tools/` (or a new module).
2. Register it in `main.py` via `mcp.tool()(my_function)`.
3. Follow the docstring/Field conventions below — the MCP client surfaces these directly to the AI assistant deciding whether/how to call the tool.

### Tool definition conventions (from README)

- Docstrings should: begin with a one-line summary, explain functionality in detail, state when to use (and not use) the tool, and include usage examples with expected input/output (see `tools/math.py::add` for the pattern).
- Parameters use `pydantic.Field` for descriptions, e.g. `param: str = Field(description="...")`.
- Always include type annotations on function arguments and return types.
