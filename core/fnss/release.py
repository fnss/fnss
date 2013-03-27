"""
This module contains all the information related to the current release of the
library including descriptions, version number, authors and contact
information. 
"""
# author information.
# Used by __init__, doc and setup
author = 'Lorenzo Saino, Cosmin Cocora'
author_email = 'fnss.dev@gmail.com'

# version information
# Used by __init__, doc and setup
version = '0.3.1'

# License information
# Used by __init__, doc and setup
license_short = 'BSD'
license_long = 'BSD license'

description_short = 'Fast creation and configuration of topologies, traffic'\
                    ' matrices and event schedules for network simulations'

description_long = """The Fast Network Simulation Setup (FNSS) core library is
a Python library providing a set of features allowing network researchers and
engineers to simplify the setup of a network simulation.

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

# URL
url = 'http://fnss.github.com/'
download_url = url
