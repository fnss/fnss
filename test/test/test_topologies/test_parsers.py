from os import environ, path
from re import findall
import unittest

import fnss

RES_DIR = environ['test.res.dir'] if 'test.res.dir' in environ else None

class Test(unittest.TestCase):

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_abilene(self):
        abilene_topo_file = path.join(RES_DIR, 'abilene-topo.txt')
        abilene_links_file = path.join(RES_DIR, 'abilene-links.txt')
        topology = fnss.parse_abilene(abilene_topo_file)
        self.assertEquals(12, topology.number_of_nodes())
        self.assertEquals(30, topology.number_of_edges())
        topology = fnss.parse_abilene(abilene_topo_file, abilene_links_file)
        self.assertEquals(12, topology.number_of_nodes())
        self.assertEquals(30, topology.number_of_edges())
        self.assertTrue(all('link_index' in topology.adj[u][v]
                            and 'link_type' in topology.adj[u][v])
                        for u, v in topology.edges())
        self.assertTrue(all(topology.adj[u][v]['length'] >= 0
                            for u, v in topology.edges()))

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_rockefuel_isp_map(self):
        rocketfuel_file = path.join(RES_DIR, 'rocketfuel-2914.cch')
        topology = fnss.parse_rocketfuel_isp_map(rocketfuel_file)
        self.assertEquals(10961, topology.number_of_nodes())
        self.assertEquals(26070, topology.number_of_edges())

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_rocketfuel_isp_latency(self):
        rocketfuel_file = path.join(RES_DIR, 'rocketfuel-1221.latencies.intra')
        topology = fnss.parse_rocketfuel_isp_latency(rocketfuel_file)
        self.assertEquals(108, topology.number_of_nodes())
        self.assertEquals(306, topology.number_of_edges())
        for _, _, data in topology.edges(data=True):
            self.assertTrue('delay' in data)
            self.assertIsInstance(data['delay'], int)
            self.assertGreaterEqual(data['delay'], 0)

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_rocketfuel_isp_latency_with_weights(self):
        latencies_file = path.join(RES_DIR, 'rocketfuel-1221.latencies.intra')
        weights_file = path.join(RES_DIR, 'rocketfuel-1221.weights.intra')
        topology = fnss.parse_rocketfuel_isp_latency(latencies_file, weights_file)
        self.assertEquals(108, topology.number_of_nodes())
        self.assertEquals(306, topology.number_of_edges())
        for _, _, data in topology.edges(data=True):
            self.assertTrue('delay' in data)
            self.assertTrue('weight' in data)
            self.assertIsInstance(data['delay'], int)
            self.assertIsInstance(data['weight'], float)
            self.assertGreaterEqual(data['delay'], 0)
            self.assertGreater(data['weight'], 0)

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_rocketfuel_isp_latency_overseas_nodes(self):
        rocketfuel_file = path.join(RES_DIR, 'rocketfuel-1239.latencies.intra')
        topology = fnss.parse_rocketfuel_isp_latency(rocketfuel_file)
        self.assertEquals(315, topology.number_of_nodes())
        self.assertEquals(1944, topology.number_of_edges())
        for _, _, data in topology.edges(data=True):
            self.assertTrue('delay' in data)
            self.assertIsInstance(data['delay'], int)
            self.assertGreaterEqual(data['delay'], 0)

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_rocketfuel_isp_latency_with_weights_overseas_nodes(self):
        latencies_file = path.join(RES_DIR, 'rocketfuel-1239.latencies.intra')
        weights_file = path.join(RES_DIR, 'rocketfuel-1239.weights.intra')
        topology = fnss.parse_rocketfuel_isp_latency(latencies_file, weights_file)
        self.assertEquals(315, topology.number_of_nodes())
        self.assertEquals(1944, topology.number_of_edges())
        for _, _, data in topology.edges(data=True):
            self.assertTrue('delay' in data)
            self.assertTrue('weight' in data)
            self.assertIsInstance(data['delay'], int)
            self.assertIsInstance(data['weight'], float)
            self.assertGreaterEqual(data['delay'], 0)
            self.assertGreater(data['weight'], 0)

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_ashiip(self):
        ashiip_file = path.join(RES_DIR, 'ashiip.txt')
        topology = fnss.parse_ashiip(ashiip_file)
        with open(ashiip_file, "r") as f:
            for line in f.readlines():
                if line.startswith(' Size :'):
                    size = int(findall('\d+', line)[0])
                    break
        print("Expected number of nodes: ", size)
        print("Actual number of nodes: ", topology.number_of_nodes())
        self.assertEqual(size, topology.number_of_nodes())
        self.assertEqual(3, topology.degree(57))

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_caida_as_relationships(self):
        caida_file = path.join(RES_DIR, 'caida-as-rel.txt')
        topology = fnss.parse_caida_as_relationships(caida_file)
        self.assertEqual(41203, topology.number_of_nodes())
        self.assertEqual(121309, topology.number_of_edges())
        self.assertEqual('customer', topology.adj[263053][28163]['type'])

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_inet(self):
        inet_file = path.join(RES_DIR, 'inet.txt')
        topology = fnss.parse_inet(inet_file)
        self.assertEqual(3500, topology.number_of_nodes())
        self.assertEqual(6146, topology.number_of_edges())

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_topology_zoo(self):
        topozoo_file = path.join(RES_DIR, 'topozoo-arnes.graphml')
        topology = fnss.parse_topology_zoo(topozoo_file)
        self.assertEqual(type(topology), fnss.Topology)
        self.assertFalse(topology.is_multigraph())
        self.assertEqual(34, topology.number_of_nodes())
        self.assertEqual(46, topology.number_of_edges())
        self.assertEqual(1000000000.0, topology.adj[4][15]['capacity'])
        self.assertEquals('bps', topology.graph['capacity_unit'])
        self.assertTrue(all(topology.adj[u][v]['length'] >= 0
                    for u, v in topology.edges()
                    if 'length' in topology.adj[u][v]))

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_topology_zoo_multigraph(self):
        topozoo_file = path.join(RES_DIR, 'topozoo-garr.graphml')
        topology = fnss.parse_topology_zoo(topozoo_file)
        self.assertEqual(type(topology), fnss.Topology)
        self.assertFalse(topology.is_multigraph())
        self.assertTrue(topology.graph['link_bundling'])
        self.assertEqual(61, topology.number_of_nodes())
        self.assertEqual(75, topology.number_of_edges())
        self.assertEquals('bps', topology.graph['capacity_unit'])
        self.assertEquals(2000000000, topology.adj[37][58]['capacity'])
        bundled_links = [(43, 18), (49, 32), (41, 18), (4, 7),
                          (6, 55), (9, 58), (58, 37), (10, 55),
                         (14, 57), (14, 35), (18, 41), (18, 43),
                         (31, 33), (31, 34), (32, 49), (37, 58)]
        for u, v in topology.edges():
            print(u, v)
            self.assertEquals((u, v) in bundled_links,
                              topology.adj[u][v]['bundle'])

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_topology_zoo_multigraph_directed_topology(self):
        topozoo_file = path.join(RES_DIR, 'topozoo-kdl.graphml')
        topology = fnss.parse_topology_zoo(topozoo_file)
        self.assertEqual(type(topology), fnss.DirectedTopology)
        self.assertFalse(topology.is_multigraph())
        self.assertTrue(topology.graph['link_bundling'])

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_brite_as(self):
        brite_file = path.join(RES_DIR, 'brite-as.brite')
        topology = fnss.parse_brite(brite_file, directed=False)
        self.assertEqual(type(topology), fnss.Topology)
        self.assertEqual(1000, topology.number_of_nodes())
        self.assertEqual(2000, topology.number_of_edges())
        # 851    570    980    2    2    851    AS_NODE
        self.assertTrue(851 in topology.nodes())
        self.assertEqual(570, topology.node[851]['longitude'])
        self.assertEqual(980, topology.node[851]['latitude'])
        self.assertEqual('AS_NODE', topology.node[851]['type'])
        # 1478    716    230    212.11553455605272    0.7075412636166207    0.0011145252848059164    716    230    E_AS    U
        self.assertEquals(1478, topology.adj[716][230]['id'])
        self.assertAlmostEquals(212.11553455605272,
                                topology.adj[716][230]['length'], 0.01)

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_brite_router(self):
        pass

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_brite_bottomup(self):
        pass

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_brite_topdown(self):
        pass
