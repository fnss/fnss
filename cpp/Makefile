SHELL = /bin/sh

VERSION = 0.4.1

# Complier options
CC      = g++
CFLAGS  = -O2
CCFLAGS = $(CFLAGS)

# Directory variables
SRC_DIR     := src
OUT_DIR     := bin
DOC_DIR      = doc
TEST_DIR     = test
DIST_DIR     = dist
LIB_DIR      = lib

EXAMPLES_SRC_DIR = examples
EXAMPLES_BIN_DIR = $(EXAMPLES_SRC_DIR)/bin

# Names of the archive and lib files
ARCHIVE_NAME  = fnss-cpp-api-$(VERSION)
LIB_NAME 	  = fnss
TEST_BIN_NAME = test

# File variables
SOURCES 		= parser.cpp traffic-matrix-sequence.cpp traffic-matrix.cpp topology.cpp application.cpp protocol-stack.cpp event-schedule.cpp event.cpp node.cpp edge.cpp property-container.cpp units.cpp measurement-unit.cpp quantity.cpp
EXAMPLE_SOURCE  = topology-example.cpp
TEST_SOURCE 	= test.cpp
OBJECTS 		= $(addprefix $(OUT_DIR)/, $(SOURCES:.cpp=.o))

.PHONY: all build dist doc test examples nitpick debug clean distclean

all: build

# Create distribution packages
dist: doc
	mkdir -p $(DIST_DIR)
	zip --exclude=$(TEST_DIR)/\* --exclude $(DIST_DIR)/\* --exclude $(OUT_DIR)/\* --exclude ".*" -r $(DIST_DIR)/$(ARCHIVE_NAME).zip *
	tar --exclude=$(TEST_DIR) --exclude=$(DIST_DIR) --exclude=$(OUT_DIR) --exclude=".*" -czf $(DIST_DIR)/$(ARCHIVE_NAME).tar.gz *

# Build documentation
doc: Doxyfile
	doxygen Doxyfile

# Build source code
build: $(OBJECTS)
	ar rcs $(OUT_DIR)/lib$(LIB_NAME).a $(OBJECTS)

# Build test code and run tests
test: build $(TEST_DIR)/$(TEST_SOURCE)
	$(CC) $(TEST_DIR)/$(TEST_SOURCE) -o $(TEST_DIR)/$(TEST_BIN_NAME) -l$(LIB_NAME) -L$(OUT_DIR) -I$(SRC_DIR) -I$(LIB_DIR)
	cd $(TEST_DIR); ./$(TEST_BIN_NAME)

# Build example
examples: build $(EXAMPLES_SRC_DIR)/$(EXAMPLE_SOURCE)
	mkdir -p $(EXAMPLES_BIN_DIR)
	$(CC) $(EXAMPLES_SRC_DIR)/$(EXAMPLE_SOURCE) -o $(EXAMPLES_BIN_DIR)/topology-example -l$(LIB_NAME) -L$(OUT_DIR) -I$(SRC_DIR) -I$(LIB_DIR);

# Clean distribution files
distclean:
	rm -rf $(DIST_DIR)

# Clean all build files
clean: distclean
	rm -rf $(OUT_DIR)
	rm -rf $(DOC_DIR)
	rm -rf $(EXAMPLES_BIN_DIR)
	rm -f $(TEST_DIR)/$(TEST_BIN_NAME)

nitpick: CFLAGS += -Wall -Werror -W
nitpick: clean all

debug: CFLAGS += -g -Wall
debug: clean all

$(OUT_DIR)/%.o : $(SRC_DIR)/%.cpp $(SRC_DIR)/%.h
	$(CC) $(CCFLAGS) -l$(OUT_DIR) -c $< -o $@ -I$(LIB_DIR)

$(OBJECTS): | $(OUT_DIR)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

