all: test
	@true

lint: style
	pylint swrelogs/

style:
	isort swrelogs/* cli.py
	black .

test:
	python -m unittest discover -s tests/* -p "test_*.py"
