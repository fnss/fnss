# Fast Network Simulation Setup
Fast Network Simulation Setup (FNSS) is a toolchain allowing network researchers
and engineers to simplify the process of setting up a network experiment scenario.
It allows users to:

* Parse a topology from a dataset or a topology generator or generate it according to a number of synthetic models
* Configure links with capacity, weights, delays and buffer sizes
* Deploy applications and protocol stacks on nodes
* Generate traffic matrices
* Generate event schedules
* Deploy network and workload configuration to a number of simulators and emulators

FNSS comprises a core library, written in Python, and a set of adapters.
This repository contains the core library, which provides all capabilities
for generating experiment scenarios and to export them to
[ns-2](http://www.isi.edu/nsnam/ns/), [Mininet](http://www.mininet.org),
[Omnet++](http://www.omnetpp.org/), [Autonetkit](http://www.autonetkit.org)
and [jFed](http://jfed.iminds.be/).
It can also be used in conjunction with the FNSS Java, C++ API or [ns-3](http://www.nsnam.org/) libraries to import topologies,
traffic matrices and event schedules in the desired target simulator or emulator.
See the repositories [fnss-java](https://github.com/fnss/fnss-java),
[fnss-cpp](https://github.com/fnss/fnss-cpp) and [fnss-ns3](https://github.com/fnss/fnss-ns3)
for further information.

## Workflow
As discussed above, the FNSS library comprises a core Python library, which also includes adapters for ns-2, Mininet and Autonetkit
and libraries for ns-3 and Java and C++ simulators/emulators.
The core Python library is needed for creating and configuring topologies, traffic matrices and event schedules.
Such objects can then be used directly if you intend to use a Python simulator.
Otherwise, they can be exported to ns-2, Autonetkit and Mininet or saved to XML files which can then be parsed by the ns-3, Java or C++ libraries.
For detailed information on how to use each component of the toolchain, please refer to
the [fnss-java](https://github.com/fnss/fnss-java), [fnss-cpp](https://github.com/fnss/fnss-cpp) or [fnss-ns3](https://github.com/fnss/fnss-ns3) repositories.
or visit the [FNSS website](http://fnss.github.io).

## Installation
The easiest way to install the latest stable version of this library is via `pip`.
First, ensure that you have Python installed on your machine with version (2.7.9+ or 3.4+).
Then, from a shell run:

    pip install --upgrade fnss

This will automatically pull the latest version and install all dependencies.

## Usage
Once the package is successfully installed, you can start using FNSS straight away.
Look at the documentation and examples for getting started. You can find the documentation online on [Read The Docs](https://fnss.readthedocs.io).

FNSS also provides a `mn-fnss` which can be used to start Mininet with
an FNSS-generated network topology.
Open a shell and run the following command to get more information on how to use it.

    $ mn-fnss --help

## Development setup
If you wish to develop on FNSS run:

    make install

This will download all development requirements and install FNSS in editable mode,
which means that any change made to the source code will be immediately available
by other libraries in the system without needing reinstallation.

You can run tests with:

    $ make test

and build documentation with:

    $ make doc

It is advisable to use [virtualenv](https://virtualenv.pypa.io/en/stable/)
to create an isolated environment for working with FNSS before running `make install`.

## Citing
If you cite FNSS in your paper, please refer to the following publication:

L. Saino, C. Cocora, G. Pavlou, [A Toolchain for Simplifying Network Simulation Setup](http://www.ee.ucl.ac.uk/~lsaino/publications/fnss-simutools13.pdf), in *Proceedings of the 6th International ICST Conference on Simulation Tools and Techniques (SIMUTOOLS '13)*, Cannes, France, March 2013

    @inproceedings{fnss,
         author = {Saino, Lorenzo and Cocora, Cosmin and Pavlou, George},
         title = {A Toolchain for Simplifying Network Simulation Setup},
         booktitle = {Proceedings of the 6th International ICST Conference on Simulation Tools and Techniques},
         series = {SIMUTOOLS '13},
         year = {2013},
         location = {Cannes, France},
         numpages = {10},
         publisher = {ICST},
         address = {ICST, Brussels, Belgium, Belgium},
    }

## Bug reports
If you wish to report a bug, please open an issue on the GitHub [issue page](https://github.com/fnss/fnss/issues/).
When reporting an issue, please try to provide a reproducible example of the problem, if possible.

## Contributions
Any contributions to the project (either bug fixes or new features) are very much welcome. To submit your code, please send a pull request on the [GitHub project page](https://github.com/fnss/fnss/).

If you wish to contribute please try to follow these guidelines:

 * Write commit messages conforming to [Git convention](http://365git.tumblr.com/post/3308646748/writing-git-commit-messages)
 * If you are sending a fix to an open issue, feel free to send a pull request directly, but make sure to reference the issue ID that you are fixing in the commit message.
 * Think about writing test cases for your feature or bug fix, if relevant. If you can't, don't worry: send your code anyway.

## License
The FNSS core library is released under the terms of the [BSD License](http://en.wikipedia.org/wiki/BSD_licenses). See `LICENSE.txt`.
