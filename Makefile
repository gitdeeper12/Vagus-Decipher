
Vagus-Decipher Makefile (BIO-MED-02)

.PHONY: help install test clean run lint format docker

help:
@echo "Available commands:"
@echo "  install     - Install dependencies"
@echo "  test        - Run tests"
@echo "  clean       - Clean temporary files"
@echo "  run         - Run example simulation"
@echo "  lint        - Run linters"
@echo "  format      - Format code"
@echo "  docker      - Build Docker image"

install:
pip install -r requirements.txt
pip install -e .

test:
pytest tests/ -v --cov=vagus_decipher

clean:
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
rm -rf pycache
rm -rf .pytest_cache
rm -rf .mypy_cache
find . -type d -name "pycache" -exec rm -rf {} + 2>/dev/null || true

run:
python examples/basic_decoding.py

lint:
ruff check vagus_decipher/
mypy vagus_decipher/

format:
black vagus_decipher/ tests/
isort vagus_decipher/ tests/

docker:
docker build -t vagus-decipher:latest .
