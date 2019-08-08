from os import environ, path
from re import findall

import pytest

import fnss
from fnss.util import extend_link_with_0_key, extend_link_tuple_to_all_parallel
# required import for pytest fixture
# noinspection PyUnresolvedReferences
from test_topologies.test_topology import use_multigraph

RES_DIR = environ['test.res.dir'] if 'test.res.dir' in environ else None

if RES_DIR is None:
    pytest.skip("Resources folder not present", allow_module_level=True)


def test_parse_abilene():
    abilene_topo_file = path.join(RES_DIR, 'abilene-topo.txt')
    abilene_links_file = path.join(RES_DIR, 'abilene-links.txt')
    topology = fnss.parse_abilene(abilene_topo_file)
    assert 12 == topology.number_of_nodes()
    assert 30 == topology.number_of_edges()
    topology = fnss.parse_abilene(abilene_topo_file, abilene_links_file)
    assert 12 == topology.number_of_nodes()
    assert 30 == topology.number_of_edges()
    assert all(({'link_index', 'link_type'} <= set(data_dict.keys())  # set() for Python 2 compatibility
                for data_dict in topology.edges.values()))
    assert all(data_dict['length'] >= 0
               for data_dict in topology.edges.values())


def test_parse_rockefuel_isp_map():
    rocketfuel_file = path.join(RES_DIR, 'rocketfuel-2914.cch')
    topology = fnss.parse_rocketfuel_isp_map(rocketfuel_file)
    assert 10961 == topology.number_of_nodes()
    assert 26070 == topology.number_of_edges()


def test_parse_rocketfuel_isp_latency():
    rocketfuel_file = path.join(RES_DIR, 'rocketfuel-1221.latencies.intra')
    topology = fnss.parse_rocketfuel_isp_latency(rocketfuel_file)
    assert 108 == topology.number_of_nodes()
    assert 306 == topology.number_of_edges()
    for _, _, data in topology.edges(data=True):
        assert 'delay' in data
        assert isinstance(data['delay'], int)
        assert data['delay'] >= 0


def test_parse_rocketfuel_isp_latency_with_weights():
    latencies_file = path.join(RES_DIR, 'rocketfuel-1221.latencies.intra')
    weights_file = path.join(RES_DIR, 'rocketfuel-1221.weights.intra')
    topology = fnss.parse_rocketfuel_isp_latency(latencies_file, weights_file)
    assert 108 == topology.number_of_nodes()
    assert 306 == topology.number_of_edges()
    for _, _, data in topology.edges(data=True):
        assert 'delay' in data
        assert 'weight' in data
        assert isinstance(data['delay'], int)
        assert isinstance(data['weight'], float)
        assert data['delay'] >= 0
        assert data['weight'] > 0


def test_parse_rocketfuel_isp_latency_overseas_nodes():
    rocketfuel_file = path.join(RES_DIR, 'rocketfuel-1239.latencies.intra')
    topology = fnss.parse_rocketfuel_isp_latency(rocketfuel_file)
    assert 315 == topology.number_of_nodes()
    assert 1944 == topology.number_of_edges()
    for _, _, data in topology.edges(data=True):
        assert 'delay' in data
        assert isinstance(data['delay'], int)
        assert data['delay'] >= 0


def test_parse_rocketfuel_isp_latency_with_weights_overseas_nodes():
    latencies_file = path.join(RES_DIR, 'rocketfuel-1239.latencies.intra')
    weights_file = path.join(RES_DIR, 'rocketfuel-1239.weights.intra')
    topology = fnss.parse_rocketfuel_isp_latency(latencies_file, weights_file)
    assert 315 == topology.number_of_nodes()
    assert 1944 == topology.number_of_edges()
    for _, _, data in topology.edges(data=True):
        assert 'delay' in data
        assert 'weight' in data
        assert isinstance(data['delay'], int)
        assert isinstance(data['weight'], float)
        assert data['delay'] >= 0
        assert data['weight'] > 0


def test_parse_ashiip():
    ashiip_file = path.join(RES_DIR, 'ashiip.txt')
    topology = fnss.parse_ashiip(ashiip_file)
    with open(ashiip_file, "r") as f:
        for line in f.readlines():
            if line.startswith(' Size :'):
                size = int(findall(r'\d+', line)[0])
                break
    print("Expected number of nodes: ", size)
    print("Actual number of nodes: ", topology.number_of_nodes())
    assert size == topology.number_of_nodes()
    assert 3 == topology.degree(57)


def test_parse_caida_as_relationships():
    caida_file = path.join(RES_DIR, 'caida-as-rel.txt')
    topology = fnss.parse_caida_as_relationships(caida_file)
    assert 41203 == topology.number_of_nodes()
    assert 121309 == topology.number_of_edges()
    assert 'customer' == topology.adj[263053][28163]['type']


def test_parse_inet():
    inet_file = path.join(RES_DIR, 'inet.txt')
    topology = fnss.parse_inet(inet_file)
    assert 3500 == topology.number_of_nodes()
    assert 6146 == topology.number_of_edges()


def test_parse_topology_zoo(use_multigraph):
    topozoo_file = path.join(RES_DIR, 'topozoo-arnes.graphml')
    topology = fnss.parse_topology_zoo(topozoo_file, use_multigraph)

    assert not topology.is_directed()
    assert use_multigraph == topology.is_multigraph()

    if use_multigraph:
        assert isinstance(topology, fnss.MultiTopology)
        assert 47 == topology.number_of_edges()

        assert 2 == len(topology.adj[4][7])
    else:
        assert isinstance(topology, fnss.Topology)
        assert 46 == topology.number_of_edges()

    assert 34 == topology.number_of_nodes()
    assert 1000000000.0 == topology.edges[extend_link_with_0_key(topology, 4, 15)]['capacity']
    assert 'bps' == topology.graph['capacity_unit']
    assert all(data_dict['length'] >= 0
               for data_dict in topology.edges.values()
               if 'length' in data_dict)


def test_parse_topology_zoo_multigraph(use_multigraph):
    topozoo_file = path.join(RES_DIR, 'topozoo-garr.graphml')
    topology = fnss.parse_topology_zoo(topozoo_file, use_multigraph)

    if use_multigraph:
        assert isinstance(topology, fnss.MultiTopology)
        assert 'link_bundling' not in topology.graph
        assert topology.is_multigraph()
        assert 89 == topology.number_of_edges()
    else:
        assert isinstance(topology, fnss.Topology)
        assert topology.graph['link_bundling']
        assert not topology.is_multigraph()
        assert 75 == topology.number_of_edges()

    assert 61 == topology.number_of_nodes()
    assert 'bps' == topology.graph['capacity_unit']
    assert 2000000000 == sum(topology.edges[link]['capacity']
                             for link in extend_link_tuple_to_all_parallel(topology, 37, 58))

    bundled_links = [(43, 18), (49, 32), (41, 18), (4, 7),
                     (6, 55), (9, 58), (58, 37), (10, 55),
                     (14, 57), (14, 35), (18, 41), (18, 43),
                     (31, 33), (31, 34), (32, 49), (37, 58)]
    for u, v in topology.edges():
        is_bundled = (u, v) in bundled_links or (v, u) in bundled_links
        if use_multigraph:
            assert is_bundled == (len(topology.adj[u][v]) > 1)
        else:
            assert is_bundled == topology.adj[u][v]['bundle']


def test_parse_topology_zoo_multigraph_directed_topology(use_multigraph):
    topozoo_file = path.join(RES_DIR, 'topozoo-kdl.graphml')
    topology = fnss.parse_topology_zoo(topozoo_file, use_multigraph)

    if use_multigraph:
        assert isinstance(topology, fnss.MultiDirectedTopology)
        assert topology.is_multigraph()
        assert 'link_bundling' not in topology.graph
    else:
        assert isinstance(topology, fnss.DirectedTopology)
        assert not topology.is_multigraph()
        assert topology.graph['link_bundling']


def test_parse_brite_as():
    brite_file = path.join(RES_DIR, 'brite-as.brite')
    topology = fnss.parse_brite(brite_file, directed=False)
    assert type(topology) == fnss.Topology
    assert 1000 == topology.number_of_nodes()
    assert 2000 == topology.number_of_edges()
    # 851    570    980    2    2    851    AS_NODE
    assert 851 in topology.nodes()
    assert 570 == topology.node[851]['longitude']
    assert 980 == topology.node[851]['latitude']
    assert 'AS_NODE' == topology.node[851]['type']
    # 1478    716    230    212.11553455605272    0.7075412636166207    0.0011145252848059164    716    230    E_AS    U
    assert 1478 == topology.adj[716][230]['id']
    assert pytest.approx(212.11553455605272, abs=0.01) == topology.adj[716][230]['length']


@pytest.mark.skip('Not implemented')
def test_parse_brite_router():
    pass


@pytest.mark.skip('Not implemented')
def test_parse_brite_bottomup():
    pass


@pytest.mark.skip('Not implemented')
def test_parse_brite_topdown():
    pass
