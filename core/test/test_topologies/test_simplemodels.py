import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
from fnss.topologies.simplemodels import *


class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_ring_topology(self):
        def test_ring_connectivity(n):
            G = ring_topology(n)
            self.assertEquals(n, G.number_of_nodes())
            self.assertEquals(n, G.number_of_edges())
            for i in range(n):
                self.assertTrue(G.has_edge(i, (i + 1) % n))
                self.assertTrue(G.has_edge(i, (i - 1) % n))
        self.assertRaises(ValueError, ring_topology, 0)
        self.assertRaises(ValueError, ring_topology, -1)
        self.assertRaises(TypeError, ring_topology, 'String')
        test_ring_connectivity(10)
        test_ring_connectivity(21)


    def test_star_topology(self):
        def test_star_connectivity(n):
            G = star_topology(n)
            self.assertEquals(n + 1, G.number_of_nodes())
            self.assertEquals(n, G.number_of_edges())
            self.assertEquals('root', G.node[0]['type'])
            for i in range(1, n+1):
                self.assertEquals('leaf', G.node[i]['type'])
                self.assertTrue(G.has_edge(i, 0))
                self.assertTrue(G.has_edge(0, i))
        self.assertRaises(ValueError, star_topology, 0)
        self.assertRaises(ValueError, star_topology, -1)
        self.assertRaises(TypeError, star_topology, 'String')
        test_star_connectivity(10)
        test_star_connectivity(21)
        
    def test_full_mesh_topology(self):
        def test_full_mesh_connectivity(n):
            G = full_mesh_topology(n)
            self.assertEquals(n, G.number_of_nodes())
            self.assertEquals((n*(n-1))//2, G.number_of_edges())
            for i in range(n):
                for j in range(n):
                    if i != j:
                        self.assertTrue(G.has_edge(i, j))
                    
        self.assertRaises(ValueError, full_mesh_topology, 0)
        self.assertRaises(ValueError, full_mesh_topology, -1)
        self.assertRaises(TypeError, full_mesh_topology, 'String')
        test_full_mesh_connectivity(10)
        test_full_mesh_connectivity(21)
        
    def test_dumbbell_topology(self):
        def test_dumbbell_connectivity(m, n):
            G = dumbbell_topology(m, n)
            self.assertEquals(2*m + n, G.number_of_nodes())
            self.assertEquals(2*m + n - 1, G.number_of_edges()) 
            for i in range(m):
                self.assertTrue(G.has_edge(i, m))
                self.assertEquals('left_bell', G.node[i]['type'])
            for i in range(m, m + n):
                self.assertTrue(G.has_edge(i, i+1))
                self.assertEquals('core', G.node[i]['type'])
            for i in range(m + n, 2*m + n):
                self.assertTrue(G.has_edge(m + n - 1, i))
                self.assertEquals('right_bell', G.node[i]['type'])
        self.assertRaises(ValueError, dumbbell_topology, 0, 0)
        self.assertRaises(ValueError, dumbbell_topology, -1, 1)
        self.assertRaises(ValueError, dumbbell_topology, 1, 3)
        self.assertRaises(TypeError, dumbbell_topology, 'String', 4)
        self.assertRaises(TypeError, dumbbell_topology, 4, 'String')
        test_dumbbell_connectivity(15, 12)
        test_dumbbell_connectivity(2, 1)
        