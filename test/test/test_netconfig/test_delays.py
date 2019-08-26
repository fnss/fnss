from functools import partial

import networkx as nx
import pytest
from pytest import approx

import fnss
from fnss.util import extend_link_tuple_to_all_parallel
from test_topologies.test_topology import duplicate_edge, get_default_edge, has_parallel_edges
# required import for pytest fixture
# noinspection PyUnresolvedReferences
from test_topologies.test_topology import use_multigraph, topology_converter


@pytest.fixture
def topology_with_distance(topology_converter, use_multigraph):
    topology = topology_converter(fnss.Topology(distance_unit='m'))
    edges = partial(get_default_edge, topology)

    return topology, edges


def test_delays_constant(topology_converter, use_multigraph):
    topo = topology_converter(fnss.k_ary_tree_topology(3, 4))
    duplicate_edge(topo, use_multigraph)

    assert topo.number_of_nodes() == (1 - 3 ** 5) // (1 - 3)
    assert topo.number_of_edges() == topo.number_of_nodes() - (0 if use_multigraph
                                                               else 1)

    with pytest.raises(ValueError):
        fnss.set_delays_constant(topo, 2, 'Km')
    odd_links = [link for link in topo.edges
                 if sum(link) % 2 == 1]
    even_links = [link for link in topo.edges
                  if sum(link) % 2 == 0]
    fnss.set_delays_constant(topo, 2, 's', odd_links)
    fnss.set_delays_constant(topo, 5000000, 'us', even_links)
    assert 's' == topo.graph['delay_unit']
    assert all(data_dict['delay'] in [2, 5]
               for data_dict in topo.edges.values())


def test_delays_geo_distance(topology_converter, use_multigraph):
    specific_delay = 1.2
    L = 5
    G_len = topology_converter(fnss.waxman_1_topology(100, L=L))
    G_xy = topology_converter(fnss.waxman_2_topology(100, domain=(0, 0, 3, 4)))
    # leave only node coordinate to trigger failure
    for data_dict in G_xy.edges.values():
        del data_dict['length']

    duplicate_edge(G_len, use_multigraph)
    duplicate_edge(G_xy, use_multigraph)

    with pytest.raises(ValueError):
        fnss.set_delays_geo_distance(G_len, 2, delay_unit='Km')
    with pytest.raises(ValueError):
        fnss.set_delays_geo_distance(G_xy, specific_delay, None, 'ms')
    fnss.set_delays_geo_distance(G_len, specific_delay,
                                 None, 'ms', links=None)
    delays = nx.get_edge_attributes(G_len, 'delay')
    assert G_len.number_of_edges() == len(delays)
    assert specific_delay * L >= max(delays.values())
    assert 0 <= min(delays.values())


def test_delays_geo_distance_conversions(topology_with_distance, use_multigraph):
    topology, _ = topology_with_distance

    topology.add_edge(1, 2, length=2000)
    # duplicate the edge, no effect for simple graphs
    topology.add_edge(1, 2, length=2000)

    specific_delay = 1.2
    fnss.set_delays_geo_distance(topology, specific_delay, None, 'us')

    assert has_parallel_edges(topology) == use_multigraph

    for link in extend_link_tuple_to_all_parallel(topology, 1, 2):
        assert topology.edges[link]['delay'] == approx(2400)
    fnss.clear_delays(topology)
    fnss.set_delays_geo_distance(topology, specific_delay, None, 's')

    for link in extend_link_tuple_to_all_parallel(topology, 1, 2):
        assert topology.edges[link]['delay'] == approx(0.0024)


def test_delays_geo_distance_conversions_partial_assignments(topology_with_distance, use_multigraph):
    topology, edges = topology_with_distance

    # duplicate the edge, no effect for simple graphs
    topology.add_edge(1, 2, length=2000)
    topology.add_edge(1, 2, length=2000)

    topology.add_edge(2, 3, length=3000)
    topology.add_edge(3, 4)

    assert has_parallel_edges(topology) == use_multigraph

    specific_delay = 1.2
    fnss.set_delays_geo_distance(topology, specific_delay,
                                 None, 'us', links=[(1, 2)])
    fnss.set_delays_geo_distance(topology, specific_delay,
                                 3, 's', links=[(2, 3), (3, 4)])
    assert topology.graph['distance_unit'] == 'm'
    assert topology.graph['delay_unit'] == 'us'
    for link in extend_link_tuple_to_all_parallel(topology, 1, 2):
        assert topology.edges[link]['delay'] == approx(2400)
    assert edges(2, 3)['delay'] == approx(3600)
    assert edges(3, 4)['delay'] == approx(3000000)


def test_delays_geo_distance_conversions_defaults(topology_with_distance, use_multigraph):
    topology, edges = topology_with_distance

    # duplicate the edge, no effect for simple graphs
    topology.add_edge(1, 2, length=2000)
    topology.add_edge(1, 2, length=2000)

    topology.add_edge(2, 3, length=3000)
    topology.add_edge(3, 4)

    assert has_parallel_edges(topology) == use_multigraph

    specific_delay = 1.2
    fnss.set_delays_geo_distance(topology, specific_delay, 3, 's', None)
    assert topology.graph['distance_unit'] == 'm'
    assert topology.graph['delay_unit'] == 's'

    for link in extend_link_tuple_to_all_parallel(topology, 1, 2):
        assert topology.edges[link]['delay'] == approx(0.0024)
    assert edges(2, 3)['delay'] == approx(0.0036)
    assert edges(3, 4)['delay'] == approx(3)


def test_clear_delays(topology_converter, use_multigraph):
    topo = topology_converter(fnss.star_topology(12))
    duplicate_edge(topo, use_multigraph)

    assert has_parallel_edges(topo) == use_multigraph

    fnss.set_delays_constant(topo, 1, 'ms', None)
    assert topo.number_of_edges() == \
           len(nx.get_edge_attributes(topo, 'delay'))
    fnss.clear_delays(topo)
    assert 0 == len(nx.get_edge_attributes(topo, 'delay'))
