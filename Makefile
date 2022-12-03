all: test
	@true

test:
	python -m unittest discover -s tests/* -p "test_*.py"
