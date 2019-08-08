import networkx as nx
import pytest

import fnss


# TODO add multigraph tests
@pytest.fixture
def topology_info():
    # set up topology used for all traffic matrix tests
    topo = fnss.k_ary_tree_topology(3, 4)
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


def test_clear_weights():
    # create new topology to avoid parameters pollution
    G = fnss.star_topology(12)
    fnss.set_weights_constant(G, 3, None)
    assert G.number_of_edges() == len(nx.get_edge_attributes(G, 'weight'))
    fnss.clear_weights(G)
    assert 0 == len(nx.get_edge_attributes(G, 'weight'))
