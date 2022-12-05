all: test
	@true

lint: style
	pylint swrelogs/

style:
	isort swrelogs/* cli.py tests/*
	black .

test:
	python -m unittest discover -b -p "test_*.py"
