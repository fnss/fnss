SHELL = /bin/bash -euo pipefail

BUILD_DIR = build
DIST_DIR  = dist
TEST_DIR  = test
DOC_DIR   = doc

.PHONY: clean dist doc test deps install upload dist-clean doc-clean

all: install

# Run all test cases
test:
	cd $(TEST_DIR); python test.py

# Build HTML documentation
doc: doc-clean
	make -C $(DOC_DIR) html

# Install Debian packages needed by Python dependencies
deps:
	apt-get update -qq
	apt-get install -y --no-install-recommends \
		libatlas-base-dev \
		liblapack-dev \
		gfortran \
		libsuitesparse-dev \
		libgdal-dev \
		graphviz \
		mono-devel

# Install the library in development mode
install:
	pip install --upgrade pip setuptools
	pip install --upgrade -r requirements.txt
	pip install --upgrade -e .

# Create distribution package
dist: clean
	python setup.py sdist bdist_wheel

# Clean documentation
doc-clean:
	make -C $(DOC_DIR) clean

# Clean dist files
dist-clean:
	rm -rf fnss.egg-info
	rm -rf $(DIST_DIR)

# Delete temp and build files
clean: doc-clean dist-clean
	find . -name "*.py[cod]" -o -name "*__pycache__" | xargs rm -rf
	rm -rf $(BUILD_DIR) MANIFEST
