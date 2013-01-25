#!/usr/bin/env python
"""
Run unit tests
"""
from os import path, getcwd, environ, mkdir
from shutil import rmtree

def run(verbosity=1, doctest=False):
    """Run tests.

    Parameters
    ----------
    verbosity: integer, optional
      Level of detail in test reports.  Higher numbers provide more detail.  

    doctest: bool, optional
      True to run doctests in code modules
    """
    try:
        import nose
    except ImportError:
        raise ImportError("The nose package is needed to run the tests.")
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
                           "Run 'nosetests' from the command line.")

    argv = [' ', '--verbosity=%d' % verbosity,
            '-w', src_dir,
            '-exe']
    if doctest:
        argv.extend(['--with-doctest','--doctest-extension=txt'])
    
    # Prepare tests
    if path.exists(tmp_dir):
        rmtree(tmp_dir)
    mkdir(tmp_dir)
    
    # Run tests
    nose.run(argv=argv)
    
    # Clean up
    if path.exists(tmp_dir):
        rmtree(tmp_dir)

if __name__=="__main__":
    run()

