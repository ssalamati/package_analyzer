build:
	python setup.py sdist bdist_wheel

install:
	pip install .

lint:
	flake8 bin/ package_analyzer/

clean:
	rm -rf build/ dist/ *.egg-info
