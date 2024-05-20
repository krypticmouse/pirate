# Define variables
PYTHON = python3
PIP = pip3
RUFF = ruff
PYRIGHT = pyright
PYTEST = pytest
MKDOCS = mkdocs

# Define targets
.PHONY: all lint type-check test build-docs serve-docs clean

all: lint fix type-check test

lint:
	$(RUFF) check .

fix:
	$(RUFF) check . --fix

type-check:
	poetry run $(PYRIGHT)

test:
	PYTHONPATH=$PYTHONPATH:. poetry run $(PYTEST) tests/

build-docs:
	$(MKDOCS) build

serve-docs:
	$(MKDOCS) serve

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf site
