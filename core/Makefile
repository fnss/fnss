SHELL = /bin/sh

BUILD_DIR = build
DIST_DIR  = dist
TEST_DIR  = test
DOC_DIR   = doc

.PHONY: clean dist doc test install upload distclean docclean

all: dist

# Run all test cases using both version 2 and 3 of Python
test:
	cd $(TEST_DIR); python test.py

# Build HTML documentation
doc: docclean
	cd $(DOC_DIR); make html

# Create distribution package
dist: clean doc
	python setup.py sdist

# Install the library
install: clean
	python setup.py install

# Upload FNSS to Python Package Index (you need access credentials)
upload: clean doc
	python setup.py sdist upload

# Clean documentation
docclean:
	cd $(DOC_DIR); make clean

# Clean dist files
distclean:
	rm -rf fnss.egg-info
	rm -rf $(DIST_DIR)

# Delete temp and build files
clean: docclean distclean
	find . -name "*__pycache__" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf
	rm -rf $(BUILD_DIR)
