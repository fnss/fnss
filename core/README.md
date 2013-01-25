# Fast Network Simulation Setup (FNSS) - Core library
The FNSS core library is a Python library providing a set of features allowing the simplification of the setup of a network simulation.
These features include the ability to:

 * Parse a topology from a dataset, a topology generator or generate it according to a number of synthetic models
 * Apply link capacity, link weights, link delays and buffer sizes
 * Deploy application stacks
 * Generate traffic matrices
 * Generate event schedules

The core library can be used in conjunction with the FNSS Java and C++ API or the ns-2 and ns-3 adapters import topologies, traffic matrices and event schedules in the desired target simulator. 

## Project directory structure
The files of the FNSS core library are organized in the following folders.

* bin: verious scripts to be run from the command shell
* dist: folder where the built packages are saved
* doc: documentation
* examples: example code using the library
* fnss: source code
* test: test code

## Install
You do not necessarily need to install FNSS to start using it. If you have already all the required packages on your system (look at requirements section below), you can simply add the directory where this README is located to your PYTHONPATH environment variable and you will be able to FNSS straight away.

However, we recommend to install FNSS using the following process, which will take care installing all required packages, if missing. 

To install the package from sources, the easiest way is to open a shell and move to the directory where this README file is located.
There should be a `setup.py` file in this directory.

To install run the following command:

`python setup.py install`

Alternatively, you can use the make script provided:

`make install`

## Build package and documentation
You do not need to build the package to use the FNSS core library: you can install it following the procedure described above. 
If you wish to build a package, for example to redistribute it, open a shell and move to the directory where this README file is located.
There should also be a `setup.py` file in this directory.

To create a package, run the following command:

`make dist`

This will create the package file and save them in the `dist` folder.
It will also generate all the HTML documentation and save it in the folder `doc/html`.
If you only want to build the documentation, run:

`make doc`

Before attempting to build the documentation make sure that you have all the packages required, listed below.

## How to use
Once the package is successfully installed, you can start using FNSS straight away.
To use the FNSS package, simply import it by typing `import fnss` or `from fnss import *` in your Python console or in your source file.
After importing the `fnss` package, all FNSS functions and classes are automatically imported. 
For furhter information on how to use library you can either look at the API documentation located in the `doc/html` folder (run `make doc` to build it). Alternatively, you can have a look at some code examples under the `examples` directory.

## Test
To run the tests, open a shell and move to the `test` subdirectory (it should contain a `test.py` file) and then run the command:

`python test.py`

Alternatively, you can use the make script provided:

`make test`

## Requirements
To run the core library of FNSS you need to have [Python](http://www.python.org/) (version 2.6 or later).
In addition you also need the following Python packages.

 * [numpy](http://www.numpy.org/) (version 1.6 or later)
 * [networkx](http://networkx.github.gov) (version 1.7 or later)
 
To run the tests, you also need the following Python packages:

 * [nose](https://nose.readthedocs.org/en/latest/) (version 1.1 or later)
 
To build the documentation from sources, you also need the following Python packages:

 * [sphinx](http://sphinx-doc.org/) (version 1.1 or later)
 * [numpydoc](http://pypi.python.org/pypi/numpydoc) (version 0.4 or later)
 
## License
The FNSS core library is released under the terms of the [BSD License](http://en.wikipedia.org/wiki/BSD_licenses). See [LICENSE.txt](LICENSE.txt)
