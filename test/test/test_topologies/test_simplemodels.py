import unittest

import fnss


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_line_topology(self):
        def test_line_connectivity(n):
            G = fnss.line_topology(n)
            self.assertEquals(n, G.number_of_nodes())
            self.assertEquals(n - 1, G.number_of_edges())
            for i in range(n):
                if i <= n - 2: self.assertTrue(G.has_edge(i, i + 1))
                if i >= 1:   self.assertTrue(G.has_edge(i, i - 1))
        self.assertRaises(ValueError, fnss.line_topology, 0)
        self.assertRaises(ValueError, fnss.line_topology, -1)
        test_line_connectivity(8)
        test_line_connectivity(11)

    def test_k_ary_tree_topology(self):
        def test_K_ary_tree_connectivity(k, h):
            expected_degree = {'root': k, 'intermediate': k + 1, 'leaf': 1}
            G = fnss.k_ary_tree_topology(k, h)
            self.assertEquals(sum(k ** d for d in range(h + 1)),
                              G.number_of_nodes())
            self.assertEquals(sum(k ** d for d in range(1, h + 1)),
                              G.number_of_edges())
            degree = G.degree()
            for v in G.nodes():
                v_type = G.node[v]['type']
                v_depth = G.node[v]['depth']
                self.assertEqual(expected_degree[v_type], degree[v])
                neighbors = G.neighbors(v)
                for u in neighbors:
                    u_depth = G.node[u]['depth']
                    if u < v:
                        self.assertEqual(u_depth, v_depth - 1)
                    elif u > v:
                        self.assertEqual(u_depth, v_depth + 1)
                    else:  # u == v
                        self.fail("Node %s has a self-loop" % str(v))
        self.assertRaises(ValueError, fnss.k_ary_tree_topology, 0, 3)
        self.assertRaises(ValueError, fnss.k_ary_tree_topology, 3, 0)
        self.assertRaises(ValueError, fnss.k_ary_tree_topology, -1, 3)
        self.assertRaises(ValueError, fnss.k_ary_tree_topology, 3, -1)
        test_K_ary_tree_connectivity(3, 5)
        test_K_ary_tree_connectivity(5, 3)
        test_K_ary_tree_connectivity(2, 1)

    def test_ring_topology(self):
        def test_ring_connectivity(n):
            G = fnss.ring_topology(n)
            self.assertEquals(n, G.number_of_nodes())
            self.assertEquals(n, G.number_of_edges())
            for i in range(n):
                self.assertTrue(G.has_edge(i, (i + 1) % n))
                self.assertTrue(G.has_edge(i, (i - 1) % n))
        self.assertRaises(ValueError, fnss.ring_topology, 0)
        self.assertRaises(ValueError, fnss.ring_topology, -1)
        self.assertRaises(TypeError, fnss.ring_topology, 'String')
        test_ring_connectivity(10)
        test_ring_connectivity(21)

    def test_star_topology(self):
        def test_star_connectivity(n):
            G = fnss.star_topology(n)
            self.assertEquals(n + 1, G.number_of_nodes())
            self.assertEquals(n, G.number_of_edges())
            self.assertEquals('root', G.node[0]['type'])
            for i in range(1, n + 1):
                self.assertEquals('leaf', G.node[i]['type'])
                self.assertTrue(G.has_edge(i, 0))
                self.assertTrue(G.has_edge(0, i))
        self.assertRaises(ValueError, fnss.star_topology, 0)
        self.assertRaises(ValueError, fnss.star_topology, -1)
        self.assertRaises(TypeError, fnss.star_topology, 'String')
        test_star_connectivity(10)
        test_star_connectivity(21)

    def test_full_mesh_topology(self):
        def test_full_mesh_connectivity(n):
            G = fnss.full_mesh_topology(n)
            self.assertEquals(n, G.number_of_nodes())
            self.assertEquals((n * (n - 1)) // 2, G.number_of_edges())
            for i in range(n):
                for j in range(n):
                    if i != j:
                        self.assertTrue(G.has_edge(i, j))
        self.assertRaises(ValueError, fnss.full_mesh_topology, 0)
        self.assertRaises(ValueError, fnss.full_mesh_topology, -1)
        self.assertRaises(TypeError, fnss.full_mesh_topology, 'String')
        test_full_mesh_connectivity(10)
        test_full_mesh_connectivity(21)

    def test_dumbbell_topology(self):
        def test_dumbbell_connectivity(m, n):
            G = fnss.dumbbell_topology(m, n)
            self.assertEquals(2 * m + n, G.number_of_nodes())
            self.assertEquals(2 * m + n - 1, G.number_of_edges())
            for i in range(m):
                self.assertTrue(G.has_edge(i, m))
                self.assertEquals('left_bell', G.node[i]['type'])
            for i in range(m, m + n):
                self.assertTrue(G.has_edge(i, i + 1))
                self.assertEquals('core', G.node[i]['type'])
            for i in range(m + n, 2 * m + n):
                self.assertTrue(G.has_edge(m + n - 1, i))
                self.assertEquals('right_bell', G.node[i]['type'])
        self.assertRaises(ValueError, fnss.dumbbell_topology, 0, 0)
        self.assertRaises(ValueError, fnss.dumbbell_topology, -1, 1)
        self.assertRaises(ValueError, fnss.dumbbell_topology, 1, 3)
        self.assertRaises(TypeError, fnss.dumbbell_topology, 'String', 4)
        self.assertRaises(TypeError, fnss.dumbbell_topology, 4, 'String')
        test_dumbbell_connectivity(15, 12)
        test_dumbbell_connectivity(2, 1)

    def test_chord_topology(self):
        def test_chord_connectivity(m, r):
            G = fnss.chord_topology(m, r)
            n = 2 ** m
            self.assertEqual(len(G), n)
            if r <= 2:
                for i in G.nodes():
                    self.assertEqual(len(G.adj[i]), m)
            else:
                for i in G.nodes():
                    for j in range(i + 1, i + r + 1):
                        self.assertTrue(G.has_edge(i, j % n))
        test_chord_connectivity(2, 1)
        test_chord_connectivity(3, 1)
        test_chord_connectivity(4, 1)
        test_chord_connectivity(5, 1)
        test_chord_connectivity(5, 2)
        test_chord_connectivity(5, 3)
        test_chord_connectivity(3, 7)

        self.assertRaises(ValueError, fnss.chord_topology, 0, 3)
        self.assertRaises(ValueError, fnss.chord_topology, 1, 3)
        self.assertRaises(ValueError, fnss.chord_topology, -1, 3)
        self.assertRaises(ValueError, fnss.chord_topology, 5, -1)
        self.assertRaises(ValueError, fnss.chord_topology, 5, 0)
        self.assertRaises(ValueError, fnss.chord_topology, 3, 8)

        self.assertRaises(TypeError, fnss.chord_topology, 5, None)
        self.assertRaises(TypeError, fnss.chord_topology, None, 3)
        self.assertRaises(TypeError, fnss.chord_topology, 5, "1")
