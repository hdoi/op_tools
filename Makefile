init:
	pip3 install -r requirements.txt

install:
	pip3 install -e .

test:
	python3 ./setup.py test

readme:
	pandoc README.md -o README.rst
