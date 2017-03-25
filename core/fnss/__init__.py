"""
The Fast Network Simulation Setup (FNSS) core library is a Python library
providing a set of features allowing network researchers and engineers to
simplify the setup of a network simulation.

These features include the ability to:

* Parse a topology from a dataset, a topology generator or generate it
  according to a number of synthetic models.
* Apply link capacities, link weights, link delays and buffer sizes.
* Deploy protocol stacks and applications on network nodes.
* Generate traffic matrices.
* Generate event schedules.

This core library includes adapters that allow users to export topologies to
ns-2, Mininet and Autonetkit.
In addition, the core library can be used in conjunction with the FNSS Java and
C++ API or the ns-3 adapter to export topologies, traffic matrices and event
schedules to the desired target simulator or emulator.
"""
# check Python version
import sys
if sys.version_info[:2] < (2, 7):
    m = "Python version 2.7 or later is required for FNSS (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

# Import release information
import fnss.release as release

__author__ = release.author
__version__ = release.version
__license__ = release.license_short

# import all subpackages and modules
from fnss.topologies import *
from fnss.netconfig import *
from fnss.traffic import *
from fnss.adapters import *
from fnss.units import *
