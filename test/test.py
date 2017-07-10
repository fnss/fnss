#!/usr/bin/env python
"""Run unit tests"""
import sys
from os import path, getcwd, environ, mkdir
from shutil import rmtree

def main():
    """Run all tests"""
    try:
        import pytest
    except ImportError:
        raise ImportError("The pytest package is needed to run the tests.")

    # get folder of Python source files
    src_dir = path.join(path.dirname(__file__), path.pardir)
    # get folder where resource files are stored and make it available to
    # test classes
    res_dir = path.abspath(path.join(path.dirname(__file__), 'resources'))
    tmp_dir = path.abspath(path.join(path.dirname(__file__), 'tmp'))
    if path.exists(res_dir):
        environ['test.res.dir'] = res_dir
    environ['test.tmp.dir'] = tmp_dir
    # stop if running from source directory
    if getcwd() == path.abspath(path.join(src_dir, path.pardir)):
        raise RuntimeError("Can't run tests from source directory.\n"
                           "Run 'py.test' from the command line.")

    # Prepare tests
    if path.exists(tmp_dir):
        rmtree(tmp_dir)
    mkdir(tmp_dir)

    # Run tests
    res = pytest.main(['.'])

    # Clean up
    if path.exists(tmp_dir):
        rmtree(tmp_dir)

    # Return results
    return res

if __name__ == "__main__":
    sys.exit(main())
