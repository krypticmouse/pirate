
# Define variables
PYTHON = python3
PIP = pip3
RUFF = ruff
PYRIGHT = pyright
PYTEST = pytest
MKDOCS = mkdocs

# Define targets
.PHONY: all lint type-check test docs clean

all: lint type-check test docs

lint:
	$(RUFF) check .

type-check:
	$(PYRIGHT) .

test:
	$(PYTEST) tests/

docs:
	$(MKDOCS) build

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf site
