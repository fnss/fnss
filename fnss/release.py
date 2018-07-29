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
version = '0.8.1'

# License information
# Used by __init__, doc and setup
license_short = 'BSD'
license_long = 'BSD license'

description_short = 'Fast creation and configuration of topologies, traffic ' \
                    'matrices and event schedules for network experiments'

description_long = """The Fast Network Simulation Setup (FNSS) core library is
a Python library providing a set of features allowing network researchers and
engineers to simplify the setup of a network experiment.

These features include the ability to:

* Parse a topology from a dataset, a topology generator or generate it
  according to a number of synthetic models.
* Apply link capacities, link weights, link delays and buffer sizes.
* Deploy protocol stacks and applications on network nodes.
* Generate traffic matrices.
* Generate event schedules.

The core library allows users to export the generated scenarios (topologies,
traffic matrices and event schedules) to ns-2, Mininet or AutoNetKit.

It also allows to save scenarios in XML files, which can be later imported
by the FNSS Java, C++ and ns-3 libraries.
"""

# URL
url = 'http://fnss.github.io/'
download_url = url
