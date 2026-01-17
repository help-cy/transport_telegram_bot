.PHONY: install run clean test lint format

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && python main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

test:
	. venv/bin/activate && pytest tests/ -v

lint:
	. venv/bin/activate && flake8 src/ --max-line-length=100

format:
	. venv/bin/activate && black src/ --line-length=100

setup:
	cp .env.example .env
	@echo "Please edit .env file and add your BOT_TOKEN"
