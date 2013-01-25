*******
Install
*******

Quick install
=============

Get NetworkX from the Python Package Index at
http://pypi.python.org/pypi/fnss

or install it with::

   easy_install fnss

and an attempt will be made to find and install an appropriate version
that matches your operating system and Python version.

More download file options are at http://fnss.github.com/

Installing from source
======================

You can install from source by downloading a source archive file
(tar.gz or zip) or by checking out the source files from the
Git source code repository.

Source archive file
-------------------

  1. Download the source (tar.gz or zip file) from
     http://pypi.python.org/pypi/fnss/ or http://fnss.github.com

  2. Unpack and change directory to the main directory
     (it should have the file setup.py).

  3. Run this instruction to build and install::
        python setup.py install


Git repository
--------------

  1. Clone the networkx repostitory::

       git clone https://github.com/fnss/fnss.git

  2. Change directory to "fnss/core"::
  
       cd fnss/core

  3.  Run::
       
       python setup.py install


If you don't have permission to install software on your
system, you can install into another directory using
the --user, --prefix, or --home flags to setup.py.

For example

::

    python setup.py install --prefix=/home/username/python
    or
    python setup.py install --home=~
    or
    python setup.py install --user

If you didn't install in the standard Python site-packages directory
you will need to set your PYTHONPATH variable to the alternate location.
See http://docs.python.org/inst/search-path.html for further details.


Requirements
============

Python
------

To use NetworkX you need Python version 2.6 or later.


Required packages
-----------------

The following packages are needed by FNSS to provide core functions.


NetworkX
^^^^^^^^

NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

  - Download: http://networkx.lanl.gov


NumPy
^^^^^

Provides matrix representation of graphs and is used in some graph algorithms for high-performance matrix computations.

  - Download: http://scipy.org/Download


SciPy
^^^^^

Provides sparse matrix representation of graphs and many numerical scientific tools.

  - Download: http://scipy.org/Download

