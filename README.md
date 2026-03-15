# run8ops

A collection of Python utilities for managing [Run 8](https://www.thedepotserver.com) operations. Data is written to `run8ops.xlsx`, with each utility populating its own sheet.

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/)

## Setup

```bash
poetry install
```

## Scripts

### `sync_yard_customer_tags.py`

Fetches the SoCal destination tags table from [thedepotserver.com](https://www.thedepotserver.com/reference/destinationtags/view/socal) and writes it to the `socal_destination_tags` sheet in `run8ops.xlsx`.

```bash
poetry run python sync_yard_customer_tags.py
```

## Development

```bash
# Run tests
poetry run pytest

# Lint
poetry run ruff check .

# Format
poetry run ruff format .
```
