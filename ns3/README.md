# FNSS ns-3 library
This library deploys FNSS topologies and event schedules XML files created using the FNSS core library into the [ns-3](https://www.nsnam.org/) simulator.

## Project directory structure
The files of the FNSS ns-3 library are organized in the following directories:

* `dist`: directory where the built packages are saved
* `fnss`: ns-3 module
 * `fnss/bindings`: Python bindings
 * `fnss/doc`: documentation
 * `fnss/examples`: examples of code
 * `fnss/helper`: source code of the helper classes
 * `fnss/model`: source code of the model classes
 * `fnss/test`: test code

## Install
To install the FNSS ns-3 library you need to have ns-3 installed on your system.
The easiest way to install the FNSS ns-3 library is to use the `Makefile` provided.

To do so, simply open the command shell, move to the directory where this README file is located and type the following command:

    $ make install NS3_DIR=/path/to/ns3/dir/

where the `NS3_DIR` attribute is path to the ns-3 directory, i.e. the directory which contains the `waf` file.

## Run
To familiarize yourself with the ns-3 library you can run the ns-3 example
that shows how to parse a topology and an event schedule and run a simple simulation.

To do that, open a shell and move to the ns-3 installation directory, i.e. the directory which contains the `waf` file. Then type:

    $ ./waf --run fnss-example

However, please not that this example has been tested successfully only with version ns-3 version 3.16. It might work on 3.17 but will certainly fail with versions 3.18 and 3.19.

## Requirements
* [ns-3](http://www.nsnam.org) (version 3.16)

## License
The FNSS ns-3 library is released under the terms of the [GNU GPLv2 license](http://www.gnu.org/licenses/gpl-2.0.html). See LICENSE.txt.
