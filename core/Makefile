BASE_DIR=`pwd`
DIST_DIR=$(BASE_DIR)/dist
TEST_DIR=$(BASE_DIR)/test
DOC_DIR=$(BASE_DIR)/doc

.PHONY: clean dist doc test install

all: dist

test:
	# Run all test cases using both version 2 and 3 of Python
	cd $(TEST_DIR); python2 test.py
	cd $(TEST_DIR); python3 test.py

doc: clean
	# Build HTML documentation
	cd $(DOC_DIR); sphinx-build . html/

dist: clean doc
	# Create distribution package
	python setup.py sdist

install: clean
	python setup.py install
	
clean:
	# Delete temp and build files
	find . -name "*__pycache__" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf
	rm -rf $(DIST_DIR)
	rm -rf $(DOC_DIR)/html
	rm -rf $(DOC_DIR)/_build
