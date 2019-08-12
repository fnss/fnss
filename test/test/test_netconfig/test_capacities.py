import pytest
from networkx import NetworkXNotImplemented

import fnss
from fnss.util import package_available
from test_topologies.test_topology import duplicate_edge, has_parallel_edges, does_not_raise
# required import for pytest fixture
# noinspection PyUnresolvedReferences
from test_topologies.test_topology import use_multigraph


class Test:
    # specifying the seeds make the topology generation deterministic
    # GLP topology has been chosen because it is always connected and
    # these parameters given a topology with large diameter and variety
    # of degrees
    # 50 nodes has been chosen because eigenvector centrality tests would
    # require considerably more time
    topo = None
    _topo_simple = fnss.glp_topology(n=50, m=1, m0=10, p=0.2, beta=-2, seed=1)

    _topo_multi = _topo_simple.to_multigraph()
    duplicate_edge(_topo_multi, True)

    capacities = [12, 25, 489, 1091]

    @pytest.fixture(autouse=True)
    def init_topo(self, use_multigraph):
        self.topo = self._topo_multi if use_multigraph \
            else self._topo_simple
        fnss.clear_capacities(self.topo)

        assert self.topo.is_multigraph() == use_multigraph
        assert has_parallel_edges(self.topo) == use_multigraph

        yield

        self.topo = None

    def test_capacities_constant(self):
        odd_links = [link for link in self.topo.edges
                     if sum(link) % 2 == 1]
        even_links = [link for link in self.topo.edges
                      if sum(link) % 2 == 0]
        fnss.set_capacities_constant(self.topo, 2, 'Mbps', odd_links)
        fnss.set_capacities_constant(self.topo, 5000, 'Kbps', even_links)
        assert 'Mbps' == self.topo.graph['capacity_unit']
        assert all(data_dict['capacity'] in [2, 5]
                   for data_dict in self.topo.edges.values())

    def test_capacities_edge_betweenness(self):
        fnss.set_capacities_edge_betweenness(self.topo, self.capacities, weighted=False)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    @pytest.mark.skipif(not package_available('scipy'), reason='Requires Scipy')
    def test_capacities_edge_communicability(self, use_multigraph):
        expectation = pytest.raises(NetworkXNotImplemented) if use_multigraph \
            else does_not_raise()
        with expectation:
            fnss.set_capacities_edge_communicability(self.topo, self.capacities)
            assert all(data_dict['capacity'] in self.capacities
                       for data_dict in self.topo.edges.values())

    @pytest.mark.skipif(not package_available('scipy'), reason='Requires Scipy')
    def test_capacities_edge_communicability_one_capacity(self, use_multigraph):
        expectation = pytest.raises(NetworkXNotImplemented) if use_multigraph \
            else does_not_raise()
        with expectation:
            fnss.set_capacities_edge_communicability(self.topo, [10])
            assert all(data_dict['capacity'] == 10
                       for data_dict in self.topo.edges.values())

    def test_capacities_betweenness_gravity(self):
        fnss.set_capacities_betweenness_gravity(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_communicability_gravity(self, use_multigraph):
        expectation = pytest.raises(NetworkXNotImplemented) if use_multigraph \
            else does_not_raise()
        with expectation:
            fnss.set_capacities_communicability_gravity(self.topo, self.capacities)
            assert all(data_dict['capacity'] in self.capacities
                       for data_dict in self.topo.edges.values())

    def test_capacities_degree_gravity(self):
        fnss.set_capacities_degree_gravity(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_eigenvector_gravity(self, use_multigraph):
        expectation = pytest.raises(NetworkXNotImplemented) if use_multigraph \
            else does_not_raise()
        with expectation:
            fnss.set_capacities_eigenvector_gravity(self.topo, self.capacities)
            assert all(data_dict['capacity'] in self.capacities
                       for data_dict in self.topo.edges.values())

    def test_capacities_eigenvector_gravity_one_capacity(self, use_multigraph):
        expectation = pytest.raises(NetworkXNotImplemented) if use_multigraph \
            else does_not_raise()
        with expectation:
            fnss.set_capacities_eigenvector_gravity(self.topo, [10])
            assert all(data_dict['capacity'] == 10
                       for data_dict in self.topo.edges.values())

    def test_capacities_pagerank_gravity(self):
        fnss.set_capacities_pagerank_gravity(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_random(self):
        with pytest.raises(ValueError):
            fnss.set_capacities_random(self.topo, {10: 0.3, 20: 0.5})
        with pytest.raises(ValueError):
            fnss.set_capacities_random(self.topo, {10: 0.3, 20: 0.8})
        fnss.set_capacities_random(self.topo, {10: 0.3, 20: 0.7})
        assert all(data_dict['capacity'] in (10, 20)
                   for data_dict in self.topo.edges.values())

    def test_capacities_random_uniform(self):
        fnss.set_capacities_random_uniform(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_random_power_law(self):
        with pytest.raises(ValueError):
            fnss.set_capacities_random_power_law(self.topo, self.capacities, alpha=0)
        with pytest.raises(ValueError):
            fnss.set_capacities_random_power_law(self.topo, self.capacities, alpha=-0.2)
        fnss.set_capacities_random_power_law(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_random_zipf(self):
        with pytest.raises(ValueError):
            fnss.set_capacities_random_zipf(self.topo, self.capacities, alpha=0)
        with pytest.raises(ValueError):
            fnss.set_capacities_random_zipf(self.topo, self.capacities, alpha=-0.2)
        fnss.set_capacities_random_zipf(self.topo, self.capacities, alpha=0.8)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())
        fnss.clear_capacities(self.topo)
        fnss.set_capacities_random_zipf(self.topo, self.capacities, alpha=1.2)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_random_zipf_mandlebrot(self):
        with pytest.raises(ValueError):
            fnss.set_capacities_random_zipf_mandelbrot(self.topo, self.capacities, alpha=0)
        with pytest.raises(ValueError):
            fnss.set_capacities_random_zipf_mandelbrot(self.topo, self.capacities, alpha=-0.2)
        with pytest.raises(ValueError):
            fnss.set_capacities_random_zipf_mandelbrot(self.topo, self.capacities, alpha=0.2, q=-0.3)
        # test with alpha=0.8 and q=2.5
        fnss.set_capacities_random_zipf_mandelbrot(self.topo, self.capacities,
                                                   alpha=0.8, q=2.5)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())
        fnss.clear_capacities(self.topo)
        # test with alpha=1.2 and q=0.4
        fnss.set_capacities_random_zipf_mandelbrot(self.topo, self.capacities,
                                                   alpha=1.2, q=0.4)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())
