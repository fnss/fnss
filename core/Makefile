SHELL = /bin/sh

DIST_DIR = dist
TEST_DIR = test
DOC_DIR  = doc

.PHONY: clean dist doc test install

all: dist

# Run all test cases using both version 2 and 3 of Python
test:
	cd $(TEST_DIR); python2 test.py
	cd $(TEST_DIR); python3 test.py

# Build HTML documentation
doc: clean
	cd $(DOC_DIR); sphinx-build . html/

# Create distribution package
dist: clean doc
	python setup.py sdist

# Install the library
install: clean
	python setup.py install

# Delete temp and build files
clean:
	find . -name "*__pycache__" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf
	rm -rf fnss.egg-info
	rm -rf $(DIST_DIR)
	rm -rf $(DOC_DIR)/html
	rm -rf $(DOC_DIR)/_build
