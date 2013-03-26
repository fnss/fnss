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

The core library can be used in conjunction with the FNSS Java and C++ API or
the ns-2 and ns-3 adapters to import topologies, traffic matrices and event
schedules in the desired target simulator.
"""
# check Python version
import sys
if sys.version_info[:2] < (2, 6):
    m = "Python version 2.6 or later is required for FNSS (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

# Import release information
from fnss.release import author, version, license_short

__author__ = author
__version__ = version
__license__ = license_short


# import all subpackages and modules
from fnss.netconfig import *
from fnss.topologies import *
from fnss.traffic import *
from fnss.util import *