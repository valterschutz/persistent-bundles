check:
    uv run ruff check --fix
    uv run ruff format
    uv run basedpyright --warnings

test:
    uv run pytest -m "not optional"

test-full:
    uv run pytest

qa: check test
qa-full: check test-full
