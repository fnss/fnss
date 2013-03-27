SHELL = /bin/sh

VERSION = 0.3.1

# Directory variables
TEST_DIR = test
DIST_DIR = dist

ARCHIVE_NAME = fnss-ns2-$(VERSION)

EXCLUDES = --exclude ".*" --exclude "__pycache__" --exclude "*.pyc" --exclude "Makefile"

.PHONY: all dist clean distclean

all: dist

# Create distribution packages
dist:
	mkdir -p $(DIST_DIR)
	zip --exclude=$(TEST_DIR)/\* --exclude $(DIST_DIR)/\* $(EXCLUDES) -r $(DIST_DIR)/$(ARCHIVE_NAME).zip *
	tar --exclude=$(TEST_DIR) --exclude=$(DIST_DIR) --exclude=$(OUT_DIR) $(EXCLUDES) -czf $(DIST_DIR)/$(ARCHIVE_NAME).tar.gz *


# Clean distribution files
distclean:
	rm -rf $(DIST_DIR)

# Clean all build files
clean: distclean

