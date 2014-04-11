*******
Install
*******

Quick install
=============

Ubuntu (version 12.04+)
-----------------------

If you use Ubuntu, you can install the FNSS core library along with the Python
interpreter and all required dependencies by running the following script::

    $ curl -L https://github.com/fnss/fnss/raw/master/core/ubuntu_install.sh | sh

You need superuser privileges to run this script.

Other operating systems
-----------------------

The easiest way to install the core Python library is to download it and install it
from the Python Package Index. To do so, you must have Python (version >= 2.6)
installed on your machine and either `pip` or `easy_install`.

To install the FNSS core library using `easy_install` open a command shell and type::

    $ easy_install fnss

If you use `pip`, type instead::

    $ pip fnss

Depending on the configuration of your machine you may need to run `pip` or `easy_install`
as superuser. Whether you use `pip` or `easy_install`, the commands reported above will
download the latest version of the FNSS core library and install it on your machine
together with all required dependencies.


Installing from source
======================

You can install from source by downloading a source archive file
(tar.gz or zip) from the `FNSS website <http://fnss.github.io>`_ or by checking out the
source files from the `GitHub repository <http://www.github.com/fnss/fnss>`_.

Source archive file
-------------------

  1. Download the source (tar.gz or zip file) from http://fnss.github.io

  2. Unpack, open a command shell and move to the main directory of the
     core library (it should have the file `setup.py`).

  3. Run this instruction to build and install::

        $ python setup.py install


Git repository
--------------

  1. Clone the FNSS repostitory::

       $ git clone https://github.com/fnss/fnss.git

  2. Change directory to *fnss/core*::
  
       $ cd fnss/core

  3.  Run::
       
       $ python setup.py install


If you don't have permission to install software on your
system, you can install into another directory using
the `--user`, `--prefix`, or `--home` flags to `setup.py`.

For example:: 

    $ python setup.py install --prefix=/home/username/python

or::
    
    $ python setup.py install --home=~
    
or::
    
    $ python setup.py install --user

If you didn't install in the standard Python site-packages directory
you will need to set your `PYTHONPATH` variable to the alternate location.
See http://docs.python.org/inst/search-path.html for further details.


Requirements
============

Python
------

To use FNSS you need Python version 2.6 or later (2.7 or later recommended).
FNSS fully supports Python 3


Required packages
-----------------

The following packages are needed by FNSS to provide core functions.


NetworkX (version >= 1.6)
^^^^^^^^^^^^^^^^^^^^^^^^^

NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

  - Download: http://networkx.github.io


NumPy (version >= 1.4)
^^^^^^^^^^^^^^^^^^^^^^

Provides matrix representation of graphs and is used in some graph algorithms for high-performance matrix computations.

  - Download: http://scipy.org/Download

Mako (version >= 0.4)
^^^^^^^^^^^^^^^^^^^^^^

It is a templating engine used to export FNSS topologies.

  - Download: http://www.makotemplates.org/download.html


