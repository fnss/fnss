.. _examples-datacenter:

Datacenter topology
===================

This example shows how to generate a datacenter topology, assign capacities
and save everything to an XML file

::

    """
    This example shows how to generate a datacenter topology, assign capacities
    and save everything to an XML file
    """
    from fnss import *
    from networkx import get_edge_attributes
    
    # create a topology with 10 core switches, 20 edge switches and 10 servers
    # per switch (i.e. 200 servers in total)
    topology = two_tier_topology(nr_core=10, nr_edge=20, nr_servers=10)
    
    # assign capcities. Assign let's set links connecting servers to edge switches
    # to 1 Gbps and links connecting core and edge switches to 10 Gbps.
    
    # get list of core_edge links and edge_leaf links
    link_types = get_edge_attributes(topology, 'type')
    core_edge_links = [link for link in link_types
                       if link_types[link] == 'core_edge']
    edge_leaf_links = [link for link in link_types
                       if link_types[link] == 'edge_leaf']
    
    # assign capacities
    set_capacities_constant(topology, 1, 'Gbps', edge_leaf_links)
    set_capacities_constant(topology, 10, 'Gbps', core_edge_links)
    
    # assign weight 1 to all links
    set_weights_constant(topology, 1)
    
    # assign delay of 10 nanoseconds to each link
    set_delays_constant(topology, 10, 'ns')
    
    # save topology to a file
    write_topology(topology, 'datacenter_topology.xml')
