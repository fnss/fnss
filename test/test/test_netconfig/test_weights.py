import networkx as nx
import pytest

import fnss
from test_topologies.test_topology import has_parallel_edges
# required import for pytest fixture
# noinspection PyUnresolvedReferences
from test_topologies.test_topology import use_multigraph, topology_converter


@pytest.fixture
def topology_info(topology_converter, use_multigraph):
    # set up topology used for all traffic matrix tests
    topo = topology_converter(fnss.k_ary_tree_topology(3, 4))

    # duplicate an edge, no effect for simple graphs
    topo.add_edge(*next(iter(topo.edges.keys()))[:2])
    assert has_parallel_edges(topo) == use_multigraph

    capacities = [10, 20]
    odd_links = [link for link in topo.edges
                 if sum(link) % 2 == 1]
    even_links = [link for link in topo.edges
                  if sum(link) % 2 == 0]
    fnss.set_capacities_random_uniform(topo, capacities)
    fnss.set_delays_constant(topo, 3, 'ms', odd_links)
    fnss.set_delays_constant(topo, 12, 'ms', even_links)

    return topo, odd_links, even_links


def test_weights_constant(topology_info):
    topo, odd_links, even_links = topology_info

    fnss.set_weights_constant(topo, 2, odd_links)
    fnss.set_weights_constant(topo, 5, even_links)
    assert all(data_dict['weight'] in [2, 5]
               for data_dict in topo.edges.values())


def test_weights_inverse_capacity(topology_info):
    topo, odd_links, even_links = topology_info
    fnss.set_weights_inverse_capacity(topo)
    assert all(data_dict['weight'] in [1, 2]
               for data_dict in topo.edges.values())


def test_weights_delays(topology_info):
    topo, odd_links, even_links = topology_info
    fnss.set_weights_delays(topo)
    assert all(data_dict['weight'] in [1, 4]
               for data_dict in topo.edges.values())


def test_clear_weights(topology_converter, use_multigraph):
    # create new topology to avoid parameters pollution
    topo = topology_converter(fnss.star_topology(12))

    # duplicate an edge, no effect for simple graphs
    topo.add_edge(*next(iter(topo.edges.keys()))[:2])
    assert has_parallel_edges(topo) == use_multigraph

    fnss.set_weights_constant(topo, 3, None)
    assert topo.number_of_edges() == len(nx.get_edge_attributes(topo, 'weight'))

    fnss.clear_weights(topo)
    assert 0 == len(nx.get_edge_attributes(topo, 'weight'))
