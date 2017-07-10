"""
Generate Event Schedule
=======================

This example shows how to generate an event schedule.

In this specific example we create a dumbbell topology, place traffic sources
on one side and traffic receivers on the other side and we generate requests
following a Poisson distribution.
"""
import fnss
import random
import networkx as nx

# generate a dumbbell topology with 5 nodes on each bell and 3 nodes on the
# connecting path
topology = fnss.dumbbell_topology(5, 3)

# assign constant weight (1) to all links
fnss.set_weights_constant(topology, 1)

# now extract links located in the edges and links in the core
# we do this easily using Python list comprehension. Each link in the dumbbell
# topology has a 'type' attribute which identifies whether it a link of the
# core path or it is in a bell.
# Look at dumbbell_topology documentation for more details.

# this return a dictionary of egdes and value of attribute type
# This function is provided by the NetworkX library.
# Since FNSS Topology and DirecteedTopology objects inherit from NetworkX's
# Graph and DiGraph, respectively, NetworkX functions can be used in FNSS too.
link_types = nx.get_edge_attributes(topology, 'type')
core_links = [links for links in link_types if link_types[links] == 'core']
edge_links = [links for links in link_types
              if link_types[links] == 'right_bell'
              or link_types[links] == 'left_bell']

# set delay equal to 1 ms in edge links and equal to 2 ms in core links
fnss.set_delays_constant(topology, 1, 'ms', edge_links)
fnss.set_delays_constant(topology, 2, 'ms', core_links)

# set capacity of 10 Mbps in edge links and 40 Mbps in core links
fnss.set_capacities_constant(topology, 10, 'Mbps', edge_links)
fnss.set_capacities_constant(topology, 40, 'Mbps', core_links)

# Now we deploy a traffic sources on right bell and traffic receivers on left
# bell
node_types = nx.get_node_attributes(topology, 'type')
left_nodes = [nodes for nodes in node_types
              if node_types[nodes] == 'left_bell']
right_nodes = [nodes for nodes in node_types
              if node_types[nodes] == 'right_bell']

for node in left_nodes:
    fnss.add_application(topology, node, 'receiver', {})

for node in right_nodes:
    fnss.add_application(topology, node, 'source', {})

# now create a function that generate events
def rand_request(source_nodes, receiver_nodes):
    source = random.choice(source_nodes)
    receiver = random.choice(receiver_nodes)
    return {'source': source, 'receiver': receiver}

event_schedule = fnss.poisson_process_event_schedule(
                        avg_interval=50,  # 50 ms
                        t_start=0,  # starts at 0
                        duration=10 * 1000,  # 10 sec
                        t_unit='ms',  # milliseconds
                        event_generator=rand_request,  # event gen function
                        source_nodes=right_nodes,  # rand_request argument
                        receiver_nodes=left_nodes  # rand_request argument
                        )
# Write topology and event schedule to files
fnss.write_topology(topology, 'topology.xml')
fnss.write_event_schedule(event_schedule, 'event_schedule.xml')




