init:
	pip3 install -r requirements.txt

install:
	pip3 install -e .

uninstall:
	pip3 uninstall op_tools

test:
	python3 ./setup.py test

doc:
	pandoc README.md -o README.rst

