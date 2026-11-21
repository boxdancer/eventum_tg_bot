.PHONY: lints

lints:
	uv run --locked ruff format .
	uv run --locked ruff check . --output-format=concise
	uv run --locked mypy . --no-pretty
