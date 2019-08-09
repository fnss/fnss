import networkx as nx
import pytest
from pytest import approx

import fnss
from fnss.util import extend_link_with_0_key


def test_delays_constant():
    topo = fnss.k_ary_tree_topology(3, 4)
    with pytest.raises(ValueError):
        fnss.set_delays_constant(topo, 2, 'Km')
    odd_links = [(u, v) for (u, v) in topo.edges()
                 if (u + v) % 2 == 1]
    even_links = [(u, v) for (u, v) in topo.edges()
                  if (u + v) % 2 == 0]
    fnss.set_delays_constant(topo, 2, 's', odd_links)
    fnss.set_delays_constant(topo, 5000000, 'us', even_links)
    assert 's' == topo.graph['delay_unit']
    assert all(data_dict['delay'] in [2, 5]
               for data_dict in topo.edges.values())


def test_delays_geo_distance():
    specific_delay = 1.2
    L = 5
    G_len = fnss.waxman_1_topology(100, L=L)
    G_xy = fnss.waxman_2_topology(100, domain=(0, 0, 3, 4))
    # leave only node coordinate to trigger failure
    for data_dict in G_xy.edges.values():
        del data_dict['length']
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


def test_delays_geo_distance_conversions():
    topology = fnss.Topology(distance_unit='m')

    def edges(u, v):
        return topology.edges[extend_link_with_0_key(topology, u, v)]

    topology.add_edge(1, 2, length=2000)
    specific_delay = 1.2
    fnss.set_delays_geo_distance(topology, specific_delay, None, 'us')
    assert edges(1, 2)['delay'] == approx (2400)
    fnss.clear_delays(topology)
    fnss.set_delays_geo_distance(topology, specific_delay, None, 's')
    assert edges(1, 2)['delay'] == approx(0.0024)


def test_delays_geo_distance_conversions_partial_assignments():
    topology = fnss.Topology(distance_unit='m')

    def edges(u, v):
        return topology.edges[extend_link_with_0_key(topology, u, v)]

    topology.add_edge(1, 2, length=2000)
    topology.add_edge(2, 3, length=3000)
    topology.add_edge(3, 4)
    specific_delay = 1.2
    fnss.set_delays_geo_distance(topology, specific_delay,
                                 None, 'us', links=[(1, 2)])
    fnss.set_delays_geo_distance(topology, specific_delay,
                                 3, 's', links=[(2, 3), (3, 4)])
    assert topology.graph['distance_unit'] == 'm'
    assert topology.graph['delay_unit'] == 'us'
    assert edges(1, 2)['delay'] == approx(2400)
    assert edges(2, 3)['delay'] == approx(3600)
    assert edges(3, 4)['delay'] == approx(3000000)


def test_delays_geo_distance_conversions_defaults():
    topology = fnss.Topology(distance_unit='m')

    def edges(u, v):
        return topology.edges[extend_link_with_0_key(topology, u, v)]

    topology.add_edge(1, 2, length=2000)
    topology.add_edge(2, 3, length=3000)
    topology.add_edge(3, 4)
    specific_delay = 1.2
    fnss.set_delays_geo_distance(topology, specific_delay, 3, 's', None)
    assert topology.graph['distance_unit'] == 'm'
    assert topology.graph['delay_unit'] == 's'
    assert edges(1, 2)['delay'] == approx(0.0024)
    assert edges(2, 3)['delay'] == approx(0.0036)
    assert edges(3, 4)['delay'] == approx(3)


def test_clear_delays():
    topo = fnss.star_topology(12)
    fnss.set_delays_constant(topo, 1, 'ms', None)
    assert topo.number_of_edges() == \
           len(nx.get_edge_attributes(topo, 'delay'))
    fnss.clear_delays(topo)
    assert 0 == len(nx.get_edge_attributes(topo, 'delay'))
