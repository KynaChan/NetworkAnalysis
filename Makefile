
default: run

install:
	poetry install --no-root

run:
	poetry run python main.py

test:
	poetry run pytest --maxfail=1 --disable-warnings -q


.PHONY: default run test install
