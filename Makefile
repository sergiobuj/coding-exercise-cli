all: test
	@true

lint: style
	pylint swrelogs/

style:
	isort --src cli.py swrelogs/*
	black .

test:
	python -m unittest discover -s tests/* -p "test_*.py"
