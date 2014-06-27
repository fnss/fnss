# Makefile with automatic targets and dependencies (*).
#
# Try 'make info' to see a build summary or 'make help' to see a list of available targets
#
# Targets:
#   lib:       built from files in $(SRC_DIR) that have both a .$(SRC_EXT) and .$(HDR_EXT)
#   bin:       built from files in $(SRC_DIR) that only have a .$(SRC_EXT)
#   doc:       build documentation using Doxygen and place it in $(DOC_DIR)
#   install:   install library, headers and executable files in *nix /usr/* dirs.
#   uninstall: revert install actions
#   examples:  compile examples in $(EXAMPLES_SRC_DIR) and put binaries in $(EXAMPLES_BUILD_DIR)
#   test:      built from *.$(SRC_EXT) in $(TEST_DIR) and executed in $(TEST_EXEC_DIR)
#              other files in $(TEST_DIR) are copied to $(TEST_EXEC_DIR) (resources, etc.)
#              see $(TEST_DIR)/test.cpp for a very simple unit-test framework
#   scratch:   built from *.$(SRC_EXT) in $(SCRATCH_DIR)
#   include:   copy-only for *.(HDR_EXT) in $(SRC_DIR)
#
# Subdirectories are supported, only caveat is don't have a duplicate name for
# things in the bin target, or it will cause overwrites in $(BIN_DIR). You can still
# get everything manually from $(BUILD_DIR) though.
#
# You can add dependencies in ./deps to get automatic -I and -L flags.
#
# (*): the only indirect (i.e. not generated straight from an #include) rule is that
#      binaries (bin, test, scratch) that include F.$(HDR_EXT) are also assumed to depend
#      on F.$(SRC_EXT) if it exists.

# Config
SHELL = /bin/sh

VERSION = 0.5.0

# NAME is used for lib$(NAME).a/.so
NAME = fnss
ARCHIVE_NAME  = fnss-cpp-api-$(VERSION)

# Compiler options
LDFLAGS  =
LDLIBS   =
# Use clang++ compiler if installed (preferred choice), fall back to g++ if not.
CLANG_INSTALLED := $(shell clang++ --version 2>/dev/null)
ifdef CLANG_INSTALLED
CXX      = clang++
CXXFLAGS = -g -O2 -Wshadow -Wall -Wfatal-errors -std=c++11 -fPIC
else
CXX      = g++
CXXFLAGS = -g -O2 -Wall -Wfatal-errors -fPIC
endif

# File extensions / ignored files.
SRC_EXT = .cpp
HDR_EXT = .h
IGNORE  = ./src/mainpage.h

# Paths. Using ./ for relative paths not optional since text must be compatible
# with find output.
SRC_DIR          = ./src
TEST_DIR         = ./test
EXAMPLES_SRC_DIR = ./examples
SCRATCH_DIR      = ./scratch
BUILD_DIR        = ./build
DEP_DIR          = ./deps
DOC_DIR          = ./doc
DIST_DIR         = ./dist
LIB_DIR          = ./lib
BIN_DIR          = ./bin
HDR_DIR          = ./include
LIB_SHARED       = $(LIB_DIR)/lib$(NAME).so
LIB_STATIC       = $(LIB_DIR)/lib$(NAME).a

# Installation dirs for *nix systems
INSTALL_LIB = /usr/lib
INSTALL_BIN = /usr/bin
INSTALL_HDR = /usr/include/$(NAME)

# Some recipes expect these to be nested in $(BUILD_DIR), so don't change them.
EXAMPLES_BUILD_DIR = $(BUILD_DIR)/examples
TEST_EXEC_DIR      = $(BUILD_DIR)/.tests
SCRATCH_BUILD_DIR  = $(BUILD_DIR)/.scratch

# Flags.
INCDIR    = $(addprefix -I, $(shell find $(DEP_DIR) -type d))
INCDIR   += $(addprefix -I, $(shell find $(SRC_DIR) -type d))
INCDIR   += -I$(TEST_DIR)
INCDIR   += -I$(EXAMPLES_SRC_DIR)
CXXFLAGS += $(INCDIR)
LDFLAGS  += $(addprefix -L, $(shell find $(DEP_DIR) -type d))

# Sources / prerequisites
SRC          := $(shell find $(SRC_DIR) -type f -name "*$(SRC_EXT)")
HDR          := $(shell find $(SRC_DIR) -type f -name "*$(HDR_EXT)")
SRC          := $(filter-out $(IGNORE), $(SRC))
HDR          := $(filter-out $(IGNORE), $(HDR))
BIN_SRC      := $(filter-out $(HDR:$(HDR_EXT)=$(SRC_EXT)), $(SRC))
SRC          := $(filter-out $(BIN_SRC), $(SRC))
EXAMPLES_SRC := $(shell find $(EXAMPLES_SRC_DIR) -type f -name "*$(SRC_EXT)")
TEST_SRC     := $(shell find $(TEST_DIR) -type f -name "*$(SRC_EXT)")
TEST_RES     := $(shell find $(TEST_DIR) -type f ! -name "*$(SRC_EXT)")
SCRATCH_SRC  := $(shell find $(SCRATCH_DIR) -type f -name "*$(SRC_EXT)" 2>/dev/null)

# Binaries / targets. _COPY for targets that just end up copying files
# List of all bin files
BIN          := $(subst $(SRC_DIR), $(BUILD_DIR), $(BIN_SRC:$(SRC_EXT)=))
OBJ          := $(subst $(SRC_DIR), $(BUILD_DIR), $(SRC:$(SRC_EXT)=.o))
EXAMPLES     := $(subst $(EXAMPLES_SRC_DIR), $(EXAMPLES_BUILD_DIR), $(EXAMPLES_SRC:$(SRC_EXT)=))
TEST         := $(subst $(TEST_DIR), $(TEST_EXEC_DIR), $(TEST_SRC:$(SRC_EXT)=))
SCRATCH      := $(subst $(SCRATCH_DIR), $(SCRATCH_BUILD_DIR), $(SCRATCH_SRC:$(SRC_EXT)=))
BIN_COPY     := $(foreach f, $(BIN), $(BIN_DIR)/$(notdir $(f)))
SCRATCH_COPY  = $(subst $(SCRATCH_BUILD_DIR), $(SCRATCH_DIR), $(SCRATCH))
HDR_COPY      = $(subst $(SRC_DIR), $(HDR_DIR), $(HDR))
TEST_RES_COPY = $(subst $(TEST_DIR), $(TEST_EXEC_DIR), $(TEST_RES))

# Build dir skeleton
BUILD_SKEL := $(shell find $(SRC_DIR) -type d ! -name .)
BUILD_SKEL := $(subst $(SRC_DIR), $(BUILD_DIR), $(BUILD_SKEL))
BUILD_SKEL += $(TEST_EXEC_DIR)
BUILD_SKEL += $(EXAMPLES_BUILD_DIR)
BUILD_SKEL += $(SCRATCH_BUILD_DIR)
BUILD_SKEL += $(subst $(TEST_DIR), $(TEST_EXEC_DIR), \
              $(shell find $(TEST_DIR) -type d ! -name .))
BUILD_SKEL += $(subst $(EXAMPLES_SRC_DIR), $(EXAMPLES_BUILD_DIR), \
              $(shell find $(EXAMPLES_SRC_DIR) -type d ! -name .))
BUILD_SKEL += $(subst $(SCRATCH_DIR), $(SCRATCH_BUILD_DIR), \
              $(shell find $(SCRATCH_DIR) -type d ! -name . 2>/dev/null))

# Auto deps
DEP = $(OBJ:=.d) $(TEST:=.d) $(EXAMPLES:=.d) $(BIN:=.d) $(SCRATCH:=.d)
-include $(DEP)

# Commands
remove_root = $(shell echo $1 | sed s/\[.]\*\[/]\*\[^/]\*\\\///)
get_src     =  $2/$(call remove_root, $(basename $1)$(SRC_EXT))
get_bin     = $(filter %$(notdir $1), $(BIN))
get_bin_dep = $(filter $(subst $(HDR_EXT),$(SRC_EXT), $(filter $(patsubst ./%,%,$(HDR)), $1)), $(patsubst ./%,%,$(SRC)))
make_dep    = @$(CXX) -MM $(CXXFLAGS) $1 > $2.d; \
              sed -i 's/.*:/$(subst /,\/,$@):/' $@.d

# Compile a file and print message. Args: <src_file> <dest_file> <cxx_options>
compile     = @echo "Compiling:   $(strip $1) -> $(strip $2): " $(shell $(call compile_cmd, $1, $2, $3))

# Actual compile task called by compile. Args: <src_file> <dest_file> <cxx_options>
compile_cmd = CMD="$(CXX) $1 $3 -o $2"; \
              $$CMD; \
              RET=$$?; \
              if [ $$RET -eq 0 ]; then \
                  echo " OK"; \
                  exit 0; \
              else \
                  echo " Error\($$CMD\)"; \
                  exit $$RET; \
              fi \

# Run test cases. Args: <test_bin_file>
run_test    = printf "Executing:   $1:  "; \
              RUN_DIR=$$(dirname $1); \
              RUN_CMD=$$(basename $1); \
              (cd $$RUN_DIR && ./$$RUN_CMD 1>/dev/null); \
              OUT=$$?; \
             if [ $$OUT -eq 0 ]; then \
                 echo "OK"; \
             else \
                 rm $1; \
                 exit 1; \
             fi \

# Summary message
SUMMARY = \
 \rBuild summary:\n \
 $(SRC_DIR)/: OBJ: $(foreach f, $(SRC), $(call remove_root, $(f)))  ->  $(LIB_STATIC) $(LIB_SHARED)\n \
 \t BIN: $(foreach f, $(BIN_SRC), $(call remove_root, $(f)))  ->  $(BIN_COPY)\n \
 \t HDR: $(foreach f, $(HDR), $(call remove_root, $(f)))  ->  $(HDR_DIR)\n \
 $(SCRATCH_DIR)/: BIN: $(foreach f, $(SCRATCH_SRC), $(call remove_root, $(f)))  ->  $(SCRATCH_COPY)\n \
 $(EXAMPLES_SRC_DIR)/: BIN: $(foreach f, $(EXAMPLES_SRC), $(call remove_root, $(f)))  ->  $(EXAMPLES)\n \
 $(TEST_DIR)/: BIN: $(foreach f, $(TEST_SRC), $(call remove_root, $(f)))  ->  $(TEST) (executed automatically)\n

# Required for dynamic prerequisites
.SECONDEXPANSION:

# Actual recipes
.PHONY: all bin bin_dir clean dist doc examples help include info install lib lib_dir scratch test test-auto uninstall

all: test-auto lib examples bin scratch include

$(BIN): %: $$(call get_src, $$@, $(SRC_DIR))
$(BIN): %: $$(call get_bin_dep, $$^) | $(OBJ) $(BUILD_DIR)
	$(eval FROM_SRC=$(call get_src, $@, $(SRC_DIR)))
	$(call make_dep, $(FROM_SRC), $@)
	$(call compile, $(FROM_SRC), $@, $(OBJ) $(CXXFLAGS) $(LDFLAGS) $(LDLIBS))

$(EXAMPLES): %: $$(call get_src, $$(call remove_root, $$@), $(EXAMPLES_SRC_DIR))
$(EXAMPLES): %: $$(call get_bin_dep, $$^) | $(OBJ) $(BUILD_DIR)
	$(eval FROM_SRC=$$(call get_src, $$(call remove_root, $$@), $(EXAMPLES_SRC_DIR)))
	$(call make_dep, $(FROM_SRC), $@)
	$(call compile, $(FROM_SRC), $@, $(OBJ) $(CXXFLAGS) $(LDFLAGS) $(LDLIBS))

$(SCRATCH): %: $$(call get_src, $$(call remove_root, $$@), $(SCRATCH_DIR))
$(SCRATCH): %: $$(call get_bin_dep, $$^) | $(OBJ) $(BUILD_DIR)
	$(eval FROM_SRC=$$(call get_src, $$(call remove_root, $$@), $(SCRATCH_DIR)))
	$(call make_dep, $(FROM_SRC), $@)
	$(call compile, $(FROM_SRC), $@, $(OBJ) $(CXXFLAGS) $(LDFLAGS) $(LDLIBS))

$(TEST): %: $$(call get_src, $$(call remove_root, $$@), $(TEST_DIR))
$(TEST): %: $$(call get_bin_dep, $$^) $(TEST_RES_COPY) | $(OBJ) $(BUILD_DIR)
	$(eval FROM_SRC=$$(call get_src, $$(call remove_root, $$@), $(TEST_DIR)))
	$(call make_dep, $(FROM_SRC), $@)
	$(call compile, $(FROM_SRC), $@, $(OBJ) $(CXXFLAGS) $(LDFLAGS) $(LDLIBS))
	@$(call run_test, $@)

$(OBJ): %.o: $$(call get_src, $$@, $(SRC_DIR)) | $(BUILD_DIR)
	$(call make_dep, $<, $@)
	$(call compile, $<, $@, -c $(CXXFLAGS))

$(TEST_RES_COPY): %: $$(subst $(TEST_EXEC_DIR), $(TEST_DIR), ./$$@) | $(BUILD_DIR)
	cp $< $@

# Add all test cases as pre-requisites.
# Tests are run automatically when building files from src
test-auto: $(TEST)

# Manually build and run test cases
test: $(TEST)
	@for t in $(TEST); do \
		$(call run_test, $$t); \
	done

# Build static and dynamic libraries
ifeq "$(strip $(OBJ))" ""
lib:
else
lib: lib_dir $(LIB_STATIC) $(LIB_SHARED)
endif

# Create lib directory
lib_dir: $(TEST)
	@if [ ! -d $(LIB_DIR) ]; then \
		mkdir -pv $(LIB_DIR); \
	fi \

# Make static library
$(LIB_STATIC): $(OBJ) $(TEST) | lib_dir
	ar rcs $(LIB_DIR)/lib$(NAME).a $(OBJ)

# Make shared object library
$(LIB_SHARED): 	$(OBJ) $(TEST) | lib_dir
	$(CXX) -shared $(OBJ) -o $(LIB_DIR)/lib$(NAME).so

# Copy executables (if any) to the bin directory
ifeq "$(strip $(BIN_COPY))" ""
bin:
else
bin: bin_dir $(BIN_COPY)
endif

# Creates bin directory
bin_dir: $(TEST)
	@if [ ! -d $(BIN_DIR) ]; then \
		mkdir -pv $(BIN_DIR); \
	fi

# Copy executables in bin directory
$(BIN_COPY): %: $$(call get_bin, $$@) $(TEST) | bin_dir
	cp $< $@

# Build examples
examples: $(EXAMPLES)

# Build scratch files
scratch: $(SCRATCH_COPY)

$(SCRATCH_COPY): %: $$(subst $(SCRATCH_DIR), $(SCRATCH_BUILD_DIR), ./$$@)
	cp $< $@

# Create include directory with all headers
include: $(HDR_COPY)

# Copy header files into include dir
$(HDR_COPY): %: $$(subst $(HDR_DIR), $(SRC_DIR), ./$$@) $(TEST)
	@if [ ! -d $(dir $@) ]; then \
		mkdir -pv $(dir $@); \
	fi
	cp $< $@

# Create build directories
$(BUILD_DIR): FORCE
	@for d in $(BUILD_SKEL); do \
		if [ ! -d $$d ]; then \
			mkdir -pv $$d; \
		fi; \
	done

# Print summary about build process
info:
	@printf "$(SUMMARY)"

# Print help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  all         to build source code, examples, run test cases and create library files"
	@echo "  doc         to build the documentation"
	@echo "  lib         to create static and dynamic library files"
	@echo "  examples    to build examples"
	@echo "  install     to install the library on your machine"
	@echo "  uninstall   to uninstall the library from your machine"
	@echo "  dist        to create distribution packages"
	@echo "  help        to show this help"
	@echo "  info        to print a build summary"
	@echo "  clean       to delete all build files and directories"

# Install library on the system
# Note: all files in the src dir with a *.(SRC_EXT) wihtout associated &.(HDR_EXT) are considered
# binary execurable files and they are copied into a folder of the PATH variable so that they
# can be run from command line by typing their name
install: $(LIB_SHARED) $(BIN_COPY) $(HDR_COPY)
	cp $(LIB_SHARED) $(INSTALL_LIB)
	if [ -d "$(BIN_DIR)" ]; then \
		cp $(BIN_DIR)/* $(INSTALL_BIN); \
	fi
	cp -r $(HDR_DIR) $(INSTALL_HDR)

# Uninstall library from the system
# Note however that if changes to the names of executables occur between
# the installation and uninstallation, old versions of renamed files remain installed
uninstall:
	rm -f $(INSTALL_LIB)/$(notdir $(LIB_SHARED))
	if [ -d "$(BIN_DIR)" ]; then \
		rm -f $(subst $(BIN_DIR), $(INSTALL_BIN), $(BIN_COPY)); \
	fi
	rm -rf $(INSTALL_HDR)

# Create distribution packages
dist:
	mkdir -pv $(DIST_DIR)
	zip --exclude $(DIST_DIR)/\* \
	    --exclude $(BIN_DIR)/\*  \
	    --exclude $(BUILD_DIR)/\* \
	    --exclude $(HDR_DIR)/\* \
	    --exclude $(LIB_DIR)/\* \
	    --exclude ".*" \
	    -r $(DIST_DIR)/$(ARCHIVE_NAME).zip *
	tar --exclude=$(subst ./,,$(DIST_DIR)) \
	    --exclude=$(subst ./,,$(BIN_DIR)) \
	    --exclude=$(subst ./,,$(BUILD_DIR)) \
	    --exclude=$(subst ./,,$(HDR_DIR)) \
	    --exclude=$(subst ./,,$(LIB_DIR)) \
	    -czf $(DIST_DIR)/$(ARCHIVE_NAME).tar.gz *

# Build documentation
doc: Doxyfile
	doxygen Doxyfile

FORCE:

# Clean all build files
clean:
	rm -rf $(DOC_DIR)
	rm -rf $(DIST_DIR)
	rm -rf $(BUILD_DIR)
	rm -rf $(LIB_DIR)
	rm -rf $(BIN_DIR)
	rm -rf $(HDR_DIR)
	@for f in $(SCRATCH); do \
		rm -fv $(SCRATCH_DIR)/$(basename $$f); \
	done
