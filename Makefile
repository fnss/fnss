SHELL = /bin/sh

VERSION = 0.2.0

CORE_DIR = core
CPP_DIR  = cpp
JAVA_DIR = java
NS2_DIR  = ns2
NS3_DIR  = ns3

DOC_DIR  = doc
DIST_DIR = dist

ARCHIVE_NAME = fnss-$(VERSION)

.PHONY: clean doc dist docclean distclean

# Build all components
all: doc dist

# Build all documentation
doc: dist docclean
	mkdir -p $(DOC_DIR)
	mkdir -p $(DOC_DIR)/core
	mkdir -p $(DOC_DIR)/java
	mkdir -p $(DOC_DIR)/cpp
	cp -r $(CORE_DIR)/doc/html/* $(DOC_DIR)/core
	cp -r $(JAVA_DIR)/doc/* $(DOC_DIR)/java
	cp -r $(CPP_DIR)/doc/html/* $(DOC_DIR)/cpp

# Collect all distribution files
dist:
	cd $(JAVA_DIR); ant
	cd $(CORE_DIR); make dist
	cd $(CPP_DIR); make dist
	cd $(NS2_DIR); make dist
	mkdir -p $(DIST_DIR)
	mkdir -p $(DIST_DIR)/core
	mkdir -p $(DIST_DIR)/java
	mkdir -p $(DIST_DIR)/cpp
	mkdir -p $(DIST_DIR)/ns2
	cp -r $(CORE_DIR)/dist/* $(DIST_DIR)/core
	cp -r $(JAVA_DIR)/dist/* $(DIST_DIR)/java
	cp -r $(CPP_DIR)/dist/* $(DIST_DIR)/cpp
	cp -r $(NS2_DIR)/dist/* $(DIST_DIR)/ns2
	zip --exclude=$(DOC_DIR)/\* --exclude $(DIST_DIR)/\* --exclude ".*" -r $(DIST_DIR)/$(ARCHIVE_NAME).zip *
	tar --exclude=$(DOC_DIR) --exclude=$(DIST_DIR) --exclude=".*" -czf $(DIST_DIR)/$(ARCHIVE_NAME).tar.gz *


# Clean centralized dist directory
distclean:
	rm -rf $(DIST_DIR)

# Clean centralized documentation directory
docclean:
	rm -rf $(DOC_DIR)

# Clean all project
clean: distclean docclean
	cd $(JAVA_DIR); ant clean
	cd $(CORE_DIR); make clean
	cd $(CPP_DIR); make clean
	cd $(NS2_DIR); make clean

