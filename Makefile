


run:
	poetry run python main.py


test:
	poetry run pytest --maxfail=1 --disable-warnings -q
