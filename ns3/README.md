# Fast Network Simulator Setup (FNSS) - ns3 adapter
This adapter deploys FNSS topology and event schedules XML files into an ns-3 simulation.

## Project directory structure
The files of the FNSS ns-3 are organized in the following directories:

* dist: directory where the built packages are saved
* fnss: ns-3 module
 * bindings: Python bindings
 * doc: documentation
 * examples: examples of code
 * helper: source code of the helper classes
 * model: source code of the model classes
 * test: test code

## Install
To install the FNSS ns-3 adapter you need to have ns-3 installed on your system.
The easiest way to install the FNSS ns-3 adapter is to use the make script provided.

To do so, simply open the command shell, move to the directory where this README file is located and type the following command:

`make install NS3_DIR=/path/to/ns3/dir/`

where the `NS3_DIR` attribute is path to the ns-3 directory, i.e. the directory which contains the `waf` file.

## Requirements
* [ns-3](http://www.nsnam.org) (version 3.16 or later)

## License
The FNSS ns-3 adapter is released under the terms of the [GNU GPLv2 license](http://www.gnu.org/licenses/gpl-2.0.html). See LICENSE.txt.
