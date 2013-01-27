# Fast Network Simulator Setup (FNSS) - ns2 adapter
This adapter converts an FNSS topology XML file into an ns-2 Tcl script.
The output Tcl script can then be run to deploy the given topology into the ns-2 simulator.

## How to use
To use the script open a command shell, move to this directory and run the command:
`python fnss-to-ns2.py -t topology.xml output.tcl`
where `topology.xml` is the XML file of the topology and `output.tcl` is the name of the desired output Tcl script. 

**Important**: In order for the script to work correctly, the input topology must staisfy certain properties:
 * each stack and each application must have a `class` attribute whose value is the ns-2 class implementing
   such stack or application, such as `Agent/TCP` or `Application/FTP`.
 * All names and values of stack and application properties must be valid properties recognized by the ns-2
   application or protocol stack.

## Requirements
* Python (version 2.6 or later)
* FNSS core library

## License
The FNSS ns-2 adapter is released under the terms of the [GNU GPLv2 license](http://www.gnu.org/licenses/gpl-2.0.html). See LICENSE.txt.
