"""
Create datacenter topology for Mininet
======================================

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
from mininet.node import OVSController


# Create FNSS topology. Let's create a simple datacenter topology
# This topology does not contain loops. If you want to use a topology with
# loops or multiple paths in Mininet you need to use a custom controller.
# More info here:
# https://github.com/mininet/mininet/wiki/Introduction-to-Mininet#multipath-routing
fnss_topo = fnss.two_tier_topology(n_core=1, n_edge=2, n_hosts=2)

# Set link attributes
fnss.set_capacities_constant(fnss_topo, 10, 'Mbps')
fnss.set_delays_constant(fnss_topo, 2, 'ms')
fnss.set_buffer_sizes_constant(fnss_topo, 50, 'packets')

# Convert FNSS topology to Mininet
# If argument relabel_nodes is set to False, node labels are not changed when
# converting an FNSS topology to a Mininet one, except converting the type to
# string (e.g. 1 -> '1'). If relabel_nodes is set to True (default option)
# then nodes are label according to Mininet conventions, e.g. hosts are
# prepended an h (e.g. 1 -> 'h1') and switches are prepended an s
# (e.g. 2 -> 's2')
mn_topo = fnss.to_mininet(fnss_topo, relabel_nodes=True)

# Create a Mininet instance and start it
# Use TCLink to implement links enables Linux Traffic Container (TC) for rate
# limitation
net = Mininet(topo=mn_topo, link=TCLink, controller=OVSController)
net.start()

# Dump host connections
dumpNodeConnections(net.hosts)

# Test network connectivity
net.pingAll()

# Test bandwidth between nodes
h1, h4 = net.get('h1', 'h4')
net.iperf((h1, h4))

# Stop Mininet
net.stop()
