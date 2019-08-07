from os import path, environ

import pytest

import fnss

TMP_DIR = environ['test.tmp.dir'] if 'test.tmp.dir' in environ else None


# TODO add multigraph tests
@pytest.fixture
def topology():
    # set up topology used for all traffic matrix tests
    topology = fnss.glp_topology(n=50, m=1, m0=10, p=0.2, beta=-2, seed=1)
    fnss.set_capacities_random(topology, {10: 0.5, 20: 0.3, 40: 0.2},
                               capacity_unit='Mbps')
    fnss.set_delays_constant(topology, 2, delay_unit='ms')
    fnss.set_weights_inverse_capacity(topology)
    for node in [2, 4, 6]:
        fnss.add_stack(topology, node, 'tcp',
                       {'protocol': 'cubic', 'rcvwnd': 1024})
    for node in [2, 4]:
        fnss.add_application(topology, node, 'client',
                             {'rate': 100, 'user-agent': 'fnss'})
    fnss.add_application(topology, 2, 'server',
                         {'port': 80, 'active': True, 'user-agent': 'fnss'})
    return topology


def test_base_topology_class():
    weight = 2
    capacity = 3
    delay = 4
    buffer_size = 5
    topology = fnss.Topology()
    topology.add_path([1, 2, 3])
    fnss.set_weights_constant(topology, weight)
    fnss.set_capacities_constant(topology, capacity)
    fnss.set_delays_constant(topology, delay)
    fnss.set_buffer_sizes_constant(topology, buffer_size)
    weights = topology.weights()
    capacities = topology.capacities()
    delays = topology.delays()
    buffer_sizes = topology.buffers()
    for e in topology.edges:
        assert weight == weights[e]
        assert capacity == capacities[e]
        assert delay == delays[e]
        assert buffer_size == buffer_sizes[e]


def test_topology_class():
    topology = fnss.Topology()
    topology.add_edge(1, 2)
    assert 1 == topology.number_of_edges()
    # add parallel link if it is multigraph
    topology.add_edge(2, 1)
    if topology.is_multigraph():
        assert 2 == topology.number_of_edges()
    else:
        assert 1 == topology.number_of_edges()

    # add 2 new nodes with string names, 2 edges for multigraph, 1 edge for simple graphs
    topology.add_edge('1', '2')
    topology.add_edge('2', '1')

    assert 4 == topology.number_of_nodes()
    if topology.is_multigraph():
        assert 4 == topology.number_of_edges()
    else:
        assert 2 == topology.number_of_edges()


def test_directed_topology_class():
    topology = fnss.DirectedTopology()
    topology.add_edge(1, 2)
    topology.add_edge(2, 1)
    assert 2 == topology.number_of_edges()


def test_od_pairs_from_topology_directed():
    dir_topology = fnss.DirectedTopology()
    dir_topology.add_edge(0, 1)
    dir_topology.add_edge(1, 0)
    dir_topology.add_edge(1, 2)
    dir_topology.add_edge(3, 2)
    dir_topology.add_edge(8, 9)
    expected_od_pairs = [(0, 1), (0, 2), (1, 0), (1, 2), (3, 2), (8, 9)]
    od_pairs = fnss.od_pairs_from_topology(dir_topology)
    assert len(expected_od_pairs) == len(od_pairs)
    for od in expected_od_pairs:
        assert od in od_pairs


def test_od_pairs_from_topology_undirected():
    topology = fnss.ring_topology(3)
    topology.add_path([7, 8, 9])  # isolated node: no flows from/to this node
    od_pairs = fnss.od_pairs_from_topology(topology)
    expected_od_pairs = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1),
                         (7, 8), (7, 9), (8, 7), (8, 9), (9, 7), (9, 8)]
    assert len(expected_od_pairs) == len(od_pairs)
    for od in expected_od_pairs:
        assert od in od_pairs


def test_fan_in_out_capacities_directed():
    dir_topology = fnss.DirectedTopology()
    dir_topology.add_edge(0, 1)
    dir_topology.add_edge(1, 0)
    dir_topology.add_edge(1, 2)
    dir_topology.add_edge(3, 2)
    fnss.set_capacities_constant(dir_topology, 10, 'Mbps')
    in_cap, out_cap = fnss.fan_in_out_capacities(dir_topology)
    assert {0: 10, 1: 10, 2: 20, 3: 0} == in_cap
    assert {0: 10, 1: 20, 2: 0, 3: 10} == out_cap


def test_fan_in_out_capacities_undirected():
    topology = fnss.star_topology(3)
    fnss.set_capacities_constant(topology, 10, 'Mbps')
    in_cap, out_cap = fnss.fan_in_out_capacities(topology)
    assert {0: 30, 1: 10, 2: 10, 3: 10} == in_cap
    assert in_cap == out_cap


@pytest.mark.skipif(TMP_DIR is None, reason="Temp folder not present")
def test_read_write_topology(topology):
    tmp_topo_file = path.join(TMP_DIR, 'toporw.xml')
    fnss.write_topology(topology, tmp_topo_file)
    assert path.exists(tmp_topo_file)
    read_topo = fnss.read_topology(tmp_topo_file)
    assert len(topology) == len(read_topo)
    assert topology.number_of_edges() == read_topo.number_of_edges()
    assert 'tcp' == fnss.get_stack(read_topo, 2)[0]
    assert 1024 == fnss.get_stack(read_topo, 2)[1]['rcvwnd']
    assert 'cubic' == fnss.get_stack(read_topo, 2)[1]['protocol']
    assert len(fnss.get_application_names(topology, 2)) == len(fnss.get_application_names(read_topo, 2))
    assert 'fnss' == fnss.get_application_properties(read_topo, 2, 'server')['user-agent']
    assert [2, 4, 6] == [v for v in read_topo.nodes()
                         if fnss.get_stack(read_topo, v) is not None
                         and fnss.get_stack(read_topo, v)[0] == 'tcp']
    assert [2, 4] == [v for v in read_topo.nodes()
                      if 'client' in fnss.get_application_names(read_topo, v)]
    assert [2] == [v for v in read_topo.nodes()
                   if 'server' in fnss.get_application_names(read_topo, v)]
