"""
Create datacenter topology for Mininet
=============================

This example shows how to create a datacenter topology with FNSS and export it
to Mininet.

This example requires Mininet to be installed on the machine. 
"""
import fnss

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


# Create FNSS topology. Let's create a simple datacenter topology
fnss_topo = fnss.two_tier_topology(n_core=2, n_edge=2, n_hosts=2)

# Set link attributes
fnss.set_capacities_constant(fnss_topo, 10, 'Mbps')
fnss.set_delays_constant(fnss_topo, 2, 'ms')
fnss.set_buffer_sizes_constant(fnss_topo, 50, 'packets')

# Convert FNSS topology to Mininet
mn_topo = fnss.to_mininet(fnss_topo)

# Create a Mininet instance and start it
# Using TCLink to implement links enables Linux Traffic Container (TC) for rate
# limitation
net = Mininet(topo=mn_topo, link=TCLink)
net.start()

# Dumping host connections
dumpNodeConnections(net.hosts)

# Test network connectivity
net.pingAll()

# Test bandwidth between nodes"
h1, h4 = net.get('1', '4')
net.iperf((h1, h4))

# Stop Mininet
net.stop()
