# Justfile for sw_rune_eval project
pytho_version := "3.11"

install:
	if [ ! -d .venv ]; then uv venv --python {{pytho_version}}; fi
	uv sync

install-dev:
	if [ ! -d .venv ]; then uv venv --python {{pytho_version}}; fi
	uv sync --extra dev

venv:
	python3 -m venv .venv

lint:
	bandit -r app

format:
	black app

run:
	uv run app/main.py
