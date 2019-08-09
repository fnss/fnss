import pytest

import fnss
from fnss.util import package_available


class Test:
    # specifying the seeds make the topology generation deterministic
    # GLP topology has been chosen because it is always connected and
    # these parameters given a topology with large diameter and variety
    # of degrees
    # 50 nodes has been chosen because eigenvector centrality tests would
    # require considerably more time
    topo = fnss.glp_topology(n=50, m=1, m0=10, p=0.2, beta=-2, seed=1)
    capacities = [12, 25, 489, 1091]

    @pytest.fixture(autouse=True)
    def clear_capacities(self):
        yield
        fnss.clear_capacities(self.topo)

    def test_capacities_constant(self):
        odd_links = [link for link in self.topo.edges
                     if (link[0] + link[1]) % 2 == 1]
        even_links = [link for link in self.topo.edges
                      if (link[0] + link[1]) % 2 == 0]
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
    def test_capacities_edge_communicability(self):
        fnss.set_capacities_edge_communicability(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    @pytest.mark.skipif(not package_available('scipy'), reason='Requires Scipy')
    def test_capacities_edge_communicability_one_capacity(self):
        fnss.set_capacities_edge_communicability(self.topo, [10])
        assert all(data_dict['capacity'] == 10
                   for data_dict in self.topo.edges.values())

    def test_capacities_betweenness_gravity(self):
        fnss.set_capacities_betweenness_gravity(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_communicability_gravity(self):
        fnss.set_capacities_communicability_gravity(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_degree_gravity(self):
        fnss.set_capacities_degree_gravity(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_eigenvector_gravity(self):
        fnss.set_capacities_eigenvector_gravity(self.topo, self.capacities)
        assert all(data_dict['capacity'] in self.capacities
                   for data_dict in self.topo.edges.values())

    def test_capacities_eigenvector_gravity_one_capacity(self):
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
