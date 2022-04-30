init:
	pip3 install -r requirements.txt

install:
	pip3 install -e .

uninstall:
	pip3 uninstall op_tools

test:
	python3 ./setup.py test

test_full:
	python3 ./setup.py test
	cd tests && python3 manual_check_sample_data_LJ.py

doc:
	pandoc README.md -o README.rst

