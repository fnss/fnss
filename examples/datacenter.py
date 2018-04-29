"""
Datacenter topology
===================

This example shows how to generate a datacenter topology, assign capacities
and save everything to an XML file
"""
import fnss
import networkx as nx

# create a topology with 10 core switches, 20 edge switches and 10 hosts
# per switch (i.e. 200 hosts in total)
topology = fnss.two_tier_topology(n_core=10, n_edge=20, n_hosts=10)

# assign capacities
# let's set links connecting servers to edge switches to 1 Gbps
# and links connecting core and edge switches to 10 Gbps.

# get list of core_edge links and edge_leaf links
link_types = nx.get_edge_attributes(topology, 'type')
core_edge_links = [link for link in link_types
                   if link_types[link] == 'core_edge']
edge_leaf_links = [link for link in link_types
                   if link_types[link] == 'edge_leaf']

# assign capacities
fnss.set_capacities_constant(topology, 1, 'Gbps', edge_leaf_links)
fnss.set_capacities_constant(topology, 10, 'Gbps', core_edge_links)

# assign weight 1 to all links
fnss.set_weights_constant(topology, 1)

# assign delay of 10 nanoseconds to each link
fnss.set_delays_constant(topology, 10, 'ns')

# save topology to a file
fnss.write_topology(topology, 'datacenter_topology.xml')
