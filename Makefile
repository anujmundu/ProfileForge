.PHONY: install dev-install format lint typecheck test coverage check dashboard clean

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

format:
	black .
	ruff check . --fix

lint:
	ruff check .

typecheck:
	mypy src

test:
	pytest

coverage:
	pytest --cov=src --cov-report=term-missing

check:
	black --check .
	ruff check .
	mypy src
	pytest

dashboard:
	python -m src.main

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
