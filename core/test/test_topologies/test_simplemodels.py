import unittest
import networkx as nx
from nose.tools import *
from fnss.topologies.simplemodels import *


class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_ring_topology(self):
        def test_ring_connectivity(n):
            G = ring_topology(n)
            assert_equals(n, G.number_of_nodes())
            assert_equals(n, G.number_of_edges())
            for i in range(n):
                assert_true(G.has_edge(i, (i + 1) % n))
                assert_true(G.has_edge(i, (i - 1) % n))
        assert_raises(ValueError, ring_topology, 0)
        assert_raises(ValueError, ring_topology, -1)
        assert_raises(TypeError, ring_topology, 'String')
        test_ring_connectivity(10)
        test_ring_connectivity(21)


    def test_star_topology(self):
        def test_star_connectivity(n):
            G = star_topology(n)
            assert_equals(n + 1, G.number_of_nodes())
            assert_equals(n, G.number_of_edges())
            assert_equals('root', G.node[0]['type'])
            for i in range(1, n+1):
                assert_equals('leaf', G.node[i]['type'])
                assert_true(G.has_edge(i, 0))
                assert_true(G.has_edge(0, i))
        assert_raises(ValueError, star_topology, 0)
        assert_raises(ValueError, star_topology, -1)
        assert_raises(TypeError, star_topology, 'String')
        test_star_connectivity(10)
        test_star_connectivity(21)
        
    def test_full_mesh_topology(self):
        def test_full_mesh_connectivity(n):
            G = full_mesh_topology(n)
            assert_equals(n, G.number_of_nodes())
            assert_equals((n*(n-1))//2, G.number_of_edges())
            for i in range(n):
                for j in range(n):
                    if i != j:
                        assert_true(G.has_edge(i, j))
                    
        assert_raises(ValueError, full_mesh_topology, 0)
        assert_raises(ValueError, full_mesh_topology, -1)
        assert_raises(TypeError, full_mesh_topology, 'String')
        test_full_mesh_connectivity(10)
        test_full_mesh_connectivity(21)
        
    def test_dumbbell_topology(self):
        def test_dumbbell_connectivity(m, n):
            G = dumbbell_topology(m, n)
            assert_equals(2*m + n, G.number_of_nodes())
            assert_equals(2*m + n - 1, G.number_of_edges()) 
            for i in range(m):
                assert_true(G.has_edge(i, m))
                assert_equals('left_bell', G.node[i]['type'])
            for i in range(m, m + n):
                assert_true(G.has_edge(i, i+1))
                assert_equals('core', G.node[i]['type'])
            for i in range(m + n, 2*m + n):
                assert_true(G.has_edge(m + n - 1, i))
                assert_equals('right_bell', G.node[i]['type'])
        assert_raises(ValueError, dumbbell_topology, 0, 0)
        assert_raises(ValueError, dumbbell_topology, -1, 1)
        assert_raises(ValueError, dumbbell_topology, 1, 3)
        assert_raises(TypeError, dumbbell_topology, 'String', 4)
        assert_raises(TypeError, dumbbell_topology, 4, 'String')
        test_dumbbell_connectivity(15, 12)
        test_dumbbell_connectivity(2, 1)
        