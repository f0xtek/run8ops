# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`run8ops` is a collection of Python utilities for managing run8 operations. Managed with **Poetry**, targeting Python 3.12+.

## Git

Use [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages:
`<type>: <description>` — e.g. `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`

## Commands

```bash
# Install dependencies
poetry install

# Run tests
pytest

# Run a single test
pytest tests/test_file.py::test_name

# Lint
ruff check .

# Format
ruff format .

# Lint + format (fix in place)
ruff check --fix . && ruff format .
```

## Architecture

The project is a collection of standalone Python scripts, each implementing a specific operational utility. Currently:

- `sync_yard_customer_tags.py` — syncs customer tag data from a yard system

Dependencies suggest scripts that scrape/parse HTML (`beautifulsoup4`) and process tabular data (`pandas`).

New utilities should follow the same pattern: a single self-contained `.py` file per task.
