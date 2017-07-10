"""
Rocketfuel topology and traffic matrix
======================================

This example shows how to import a topology from RocketFuel, configure it
(assign capacities, weights and delays), generate a traffic matrix and
save topology and traffic matrix to XML files.
"""
import fnss
import random

# Import RocketFuel topology
# Replace the filename with the actual location of the file you want to parse
topology = fnss.parse_rocketfuel_isp_map("rocket-fuel-topo-file.cch")

# add capacities
capacities = [1, 10, 40]
capacity_unit = 'Gbps'
fnss.set_capacities_edge_betweenness(topology, capacities, capacity_unit,
                                weighted=False)

# add weights proportional to inverse of capacity
fnss.set_weights_inverse_capacity(topology)

# add constant link delays of 2 ms
fnss.set_delays_constant(topology, 2, delay_unit='ms')

# generate cyclostationary traffic matrix (period 7 days, 24 samples per day)
tmc = fnss.sin_cyclostationary_traffic_matrix(
       topology,
       mean=0.5,  # average flow in TM is 0,5 Gbps
       stddev=0.05,  # this is the std among average flows of different OD pairs
       gamma=0.8,  # gamma and log_psi are parameters for fitting the std of
       log_psi=-0.33,  # volume fluctuations over time. Look at Nucci et al. paper
       delta=0.2,  # traffic variation from period max and avg as fraction of average
       n=24,  # number of samples per each period
       periods=7,  # number of periods
       max_u=0.9,  # max link utilization desired
       origin_nodes=None,  # Specify origin and destination nodes. If None,
       destination_nodes=None  # all nodes of the topology are both
       )  # origin and destination nodes of traffic


# now we generate a static traffic matrix, but this time instead of generating
# a matrix where all nodes are both origin and destinations, we pick up only
# few nodes as sources and destinations of traffic.
# Let's select 5 sources and 5 destinations
nodes = topology.nodes()
origins = random.sample(nodes, 5)
destinations = random.sample(nodes, 5)
# generate traffic matrix
tms = fnss.static_traffic_matrix(topology, mean=0.5, stddev=0.05, max_u=0.9,
                                 origin_nodes=origins,
                                 destination_nodes=destinations)

# save topology on a file
fnss.write_topology(topology, 'topology.xml')

# save traffic matrices on files
fnss.write_traffic_matrix(tmc, 'cyclostationary-traffic-matrix.xml')
fnss.write_traffic_matrix(tms, 'static-traffic-matrix.xml')
