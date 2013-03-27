SHELL = /bin/sh

VERSION = 0.3.1

SRC_DIR  = fnss
DIST_DIR = dist
DOC_DIR = doc
ARCHIVE_NAME = fnss-ns3-$(VERSION)

.PHONY: clean dist distclean doc docclean install test uninstall

all: install dist

# Install module in ns-3
install:
	rm -rf $(NS3_DIR)/src/$(SRC_DIR)
	cp -r fnss $(NS3_DIR)/src 
	cd $(NS3_DIR); \
	./waf configure --enable-examples --enable-tests; \
	./waf build

# Uninstall module from ns-3
uninstall:
	rm -rf $(NS3_DIR)/src/$(SRC_DIR)
	cd $(NS3_DIR); \
	./waf configure --enable-examples --enable-tests; \
	./waf build
    
# Ru ns-3 tests
test: install
	cd $(NS3_DIR); ./test.py

# Build documeantion
doc: Doxyfile
	doxygen Doxyfile

# Build packages for distribution
dist: distclean
	mkdir -p $(DIST_DIR)
	zip --exclude ".*" --exclude $(DIST_DIR)/\* -r $(DIST_DIR)/$(ARCHIVE_NAME).zip *
	tar --exclude=".*" --exclude=$(DIST_DIR) -czf $(DIST_DIR)/$(ARCHIVE_NAME).tar.gz *

# Clean distribution packages
distclean:
	rm -rf $(DIST_DIR)

# Clean documentation
docclean:
	rm -rf $(DOC_DIR)

# Clean all adapter
clean: distclean docclean
	find . -name "*__pycache__" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf

