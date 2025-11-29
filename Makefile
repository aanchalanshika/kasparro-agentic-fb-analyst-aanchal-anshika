# Makefile for Kasparro Agentic Facebook Analyst

.PHONY: help setup install run test lint clean all

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup       - Create virtual environment and install dependencies"
	@echo "  make install     - Install dependencies only (venv must exist)"
	@echo "  make run         - Run the analysis with default query"
	@echo "  make run-custom  - Run with custom query (use QUERY='your query')"
	@echo "  make test        - Run all tests"
	@echo "  make lint        - Check code quality with flake8"
	@echo "  make clean       - Remove generated files and caches"
	@echo "  make all         - Setup + test + lint"

# Setup: Create venv and install dependencies
setup:
	@echo "Creating virtual environment..."
	python -m venv .venv
	@echo "Installing dependencies..."
	.venv\Scripts\pip install -r requirements.txt
	@echo "✅ Setup complete! Activate with: .venv\Scripts\activate"

# Install dependencies only
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Run analysis with default query
run:
	@echo "Running analysis: 'Analyze ROAS drop in last 7 days'"
	python run.py "Analyze ROAS drop in last 7 days"
	@echo "✅ Check reports/ for outputs"

# Run with custom query
run-custom:
	@echo "Running custom analysis: $(QUERY)"
	python run.py "$(QUERY)"

# Run all tests
test:
	@echo "Running tests..."
	pytest tests/ -v
	@echo "✅ Tests complete!"

# Lint code
lint:
	@echo "Checking code quality..."
	flake8 src/ tests/ --max-line-length=120 --ignore=E501,W503
	@echo "✅ Lint check complete!"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	if exist reports\*.json del /Q reports\*.json
	if exist reports\*.md del /Q reports\*.md
	if exist logs\*.json del /Q logs\*.json
	if exist __pycache__ rmdir /S /Q __pycache__
	if exist .pytest_cache rmdir /S /Q .pytest_cache
	if exist src\__pycache__ rmdir /S /Q src\__pycache__
	if exist src\agents\__pycache__ rmdir /S /Q src\agents\__pycache__
	if exist src\orchestrator\__pycache__ rmdir /S /Q src\orchestrator\__pycache__
	if exist tests\__pycache__ rmdir /S /Q tests\__pycache__
	@echo "✅ Cleanup complete!"

# Setup + test + lint
all: setup test lint
	@echo "✅ All tasks complete!"

# Example usage targets
example-roas:
	python run.py "Why did ROAS drop?"

example-ctr:
	python run.py "Why is CTR low and how to improve it?"

example-full:
	python run.py "Analyze campaign performance and suggest creative improvements"
