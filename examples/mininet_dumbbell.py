"""
Create dumbbell topology for Mininet
====================================

This example shows how to create a dumbbell topology with FNSS and export it
to Mininet.

This example requires Mininet to be installed on the machine.
"""
import networkx as nx
import fnss

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController


# Create FNSS topology. Let's create a simple dumbbell topology
# This topology does not contain loops. If you want to use a topology with
# loops or multiple paths in Mininet you need to use a custom controller.
# More info here:
# https://github.com/mininet/mininet/wiki/Introduction-to-Mininet#multipath-routing
fnss_topo = fnss.dumbbell_topology(5, 4)

# now extract links located in the edges and links in the core
# we do this easily using Python list comprehension. Each link in the dumbbell
# topology has a 'type' attribute which identifies whether it a link of the
# core path or it is in a bell.
# Look at dumbbell_topology documentation for more details.

# this return a dictionary of egdes and value of attribute type
# This function is provided by the NetworkX library.
# Since FNSS Topology and DirecteedTopology objects inherit from NetworkX's
# Graph and DiGraph, respectively, NetworkX functions can be used in FNSS too.
link_types = nx.get_edge_attributes(fnss_topo, 'type')
core_links = [links for links in link_types if link_types[links] == 'core']
edge_links = [links for links in link_types
              if link_types[links] == 'right_bell'
              or link_types[links] == 'left_bell']

# set delay equal to 1 ms in edge links and equal to 2 ms in core links
fnss.set_delays_constant(fnss_topo, 1, 'ms', edge_links)
fnss.set_delays_constant(fnss_topo, 2, 'ms', core_links)

# set capacity of 10 Mbps in edge links and 40 Mbps in core links
fnss.set_capacities_constant(fnss_topo, 10, 'Mbps', edge_links)
fnss.set_capacities_constant(fnss_topo, 40, 'Mbps', core_links)

# Set buffer size constant to all interfaces
fnss.set_buffer_sizes_constant(fnss_topo, 50, 'packets')

# Now we deploy a traffic sources on right bell and traffic receivers on left
# bell
node_types = nx.get_node_attributes(fnss_topo, 'type')
core_nodes = [nodes for nodes in node_types
              if node_types[nodes] == 'core']
left_nodes = [nodes for nodes in node_types
              if node_types[nodes] == 'left_bell']
right_nodes = [nodes for nodes in node_types
              if node_types[nodes] == 'right_bell']

# Set nodes on bells to be hosts and nodes on bottleneck path to be switches.
# Differently from datacenter topologies, which already provide annotation of
# what nodes are hosts and switches, we need to explicitly tell which nodes
# are switches and which are hosts to deploy the topology in Mininet
hosts = left_nodes + right_nodes
switches = core_nodes

# Convert FNSS topology to Mininet
# If argument relabel_nodes is set to False, node labels are not changed when
# converting an FNSS topology to a Mininet one, except converting the type to
# string (e.g. 1 -> '1'). If relabel_nodes is set to True (default option)
# then nodes are label according to Mininet conventions, e.g. hosts are
# prepended an h (e.g. 1 -> 'h1') and switches are prepended an s
# (e.g. 2 -> 's2')
mn_topo = fnss.to_mininet(fnss_topo,
                          switches=switches,
                          hosts=hosts,
                          relabel_nodes=True)

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
h1, h8 = net.get('h1', 'h8')
net.iperf((h1, h8))

# Stop Mininet
net.stop()
