# Makefile for Sphinx documentation
SHELL = /bin/sh

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = fnss
SOURCEDIR     = source
BUILDDIR      = build

SCRIPTSDIR    = scripts
EXCODEDIR     = ../examples
EXSRCDOCDIR   = $(SOURCEDIR)/examples
GENAPIDOCDIR  = $(SOURCEDIR)/apidoc/generated
TMPDIR        = tmp


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Autogenerate documentation for examples and all classes and functions
init:
	rm -rf $(TMPDIR)
	rm -rf $(EXSRCDOCDIR)
	rm -rf $(GENAPIDOCDIR)
	mkdir -p $(TMPDIR)
	cp $(SOURCEDIR)/conf.py $(TMPDIR)/conf.py
	python $(SCRIPTSDIR)/make_apidoc.py $(TMPDIR)/index.rst $(GENAPIDOCDIR)
	sphinx-build -b linkcheck $(TMPDIR) $(BUILDDIR)
	rm -rf $(TMPDIR)
	python $(SCRIPTSDIR)/make_examples.py $(EXCODEDIR) $(EXSRCDOCDIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile init
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
