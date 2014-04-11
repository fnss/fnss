************************************
Fast Network Simulation Setup (FNSS)
************************************

This is the documentation of the FNSS core library.
It is a Python library providing a set of features allowing to simplify the setup of a network experiment.
These features include the ability to:

* Parse a topology from a dataset, a topology generator or generate it according to a number of synthetic models
* Apply link capacity, link weights, link delays and buffer sizes
* Deploy application stacks
* Generate traffic matrices
* Generate event schedules

The core libary in addition to the features listed above, contains adapters to export generated scnearios to a the following network simulators or emulators: `ns-2 <http://www.isi.edu/nsnam/ns/>`_, `Mininet <http://www.mininet.org/>`_ and `Autonetkit <http://www.autonetkit.org/>`_.
Generated expriment scenarios (i.e. topologies, event schedules and traffic matrices) can be saved into XML files and then imported by libraries written in other languages. Currently, FNSS provides generic Java and C++ libraries as well as a C++ library specific for the `ns-3 <http://www.nsnam.org/>`_ simulator.
These libraries can be downloaded from the `FNSS website <http://fnss.github.io/>`_.

The FNSS core library is released under the terms of the `BSD license <https://raw.github.com/fnss/fnss/master/core/LICENSE.txt>`_.

If you use FNSS for your paper, please cite the following publication:

.. highlights::

    Lorenzo Saino, Cosmin Cocora and George Pavlou, 
    `A Toolchain for Symplifying Network Simulation Setup <http://www.ee.ucl.ac.uk/~lsaino/publications/fnss-simutools13.pdf>`_,
    in *Proceedings of the 6th International ICST Conference on Simulation Tools and Techniques (SIMUTOOLS ‘13)*, 
    Cannes, France, March 2013

The BibTeX entry is::

    @inproceedings{fnss,
         author = {Saino, Lorenzo and Cocora, Cosmin and Pavlou, George},
         title = {A Toolchain for Simplifying Network Simulation Setup},
         booktitle = {Proceedings of the 6th International ICST Conference on Simulation Tools and Techniques},
         series = {SIMUTOOLS '13},
         year = {2013},
         location = {Cannes, France},
         numpages = {10},
         publisher = {ICST (Institute for Computer Sciences, Social-Informatics and Telecommunications Engineering)},
         address = {ICST, Brussels, Belgium, Belgium},
    } 

Contents
========

.. toctree::
   :maxdepth: 4

   architecture
   install
   apidoc/index
   examples/index

    
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
