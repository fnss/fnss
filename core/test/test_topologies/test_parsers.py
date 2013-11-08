import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
from os import environ, path
from re import findall
import fnss

RES_DIR = environ['test.res.dir'] if 'test.res.dir' in environ else None

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


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
        self.assertTrue(all('link_index' in topology.edge[u][v]
                            and 'link_type' in topology.edge[u][v])
                        for u, v in topology.edges_iter())
        self.assertTrue(all(topology.edge[u][v]['length'] >= 0
                            for u,v in topology.edges_iter()))


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_rockefuel_isp_map(self):
        rocketfuel_file = path.join(RES_DIR, 'rocketfuel-2914.cch')
        topology = fnss.parse_rocketfuel_isp_map(rocketfuel_file)
        self.assertEquals(10961, topology.number_of_nodes())
        self.assertEquals(26070, topology.number_of_edges())


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
        caida_file = path.join(RES_DIR,'caida-as-rel.txt')
        topology = fnss.parse_caida_as_relationships(caida_file)
        self.assertEqual(41203, topology.number_of_nodes())
        self.assertEqual(121309, topology.number_of_edges())
        self.assertEqual('customer',topology.edge[263053][28163]['type'])


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_inet(self):
        inet_file = path.join(RES_DIR,'inet.txt')
        topology = fnss.parse_inet(inet_file)
        self.assertEqual(3500, topology.number_of_nodes())
        self.assertEqual(6146, topology.number_of_edges())


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_topology_zoo(self):
        topozoo_file = path.join(RES_DIR,'topozoo-arnes.graphml')
        topology = fnss.parse_topology_zoo(topozoo_file)
        self.assertEqual(type(topology), fnss.Topology)
        self.assertFalse(topology.is_multigraph())
        self.assertEqual(34, topology.number_of_nodes())
        self.assertEqual(46, topology.number_of_edges())
        self.assertEqual(1000000000.0, topology.edge[4][15]['capacity'])
        self.assertEquals('bps', topology.graph['capacity_unit'])
        self.assertTrue(all(topology.edge[u][v]['length'] >= 0
                    for u,v in topology.edges_iter()
                    if 'length' in topology.edge[u][v]))

    
    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_topology_zoo_multigraph(self):
        topozoo_file = path.join(RES_DIR,'topozoo-garr.graphml')
        topology = fnss.parse_topology_zoo(topozoo_file)
        self.assertEqual(type(topology), fnss.Topology)
        self.assertFalse(topology.is_multigraph())
        self.assertEqual(61, topology.number_of_nodes())
        self.assertEqual(75, topology.number_of_edges())
        self.assertEquals('bps', topology.graph['capacity_unit'])
        self.assertEquals(2000000000, topology.edge[37][58]['capacity'])
        bundled_links = [(43, 18), (49, 32), (41, 18),   (4, 7),
                          (6, 55),  (9, 58), (58, 37), (10, 55),
                         (14, 57), (14, 35), (18, 41), (18, 43),
                         (31, 33), (31, 34), (32, 49), (37, 58)]
        for u, v in topology.edges():
            print(u, v)
            self.assertEquals((u, v) in bundled_links,
                              topology.edge[u][v]['bundle'])


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_brite_as(self):
        brite_file = path.join(RES_DIR,'brite-as.brite')
        topology = fnss.parse_brite(brite_file, directed=False)
        self.assertEqual(type(topology), fnss.Topology)
        self.assertEqual(1000, topology.number_of_nodes())
        self.assertEqual(2000, topology.number_of_edges())
        #851    570    980    2    2    851    AS_NODE
        self.assertTrue(851 in topology.nodes())
        self.assertEqual(570, topology.node[851]['longitude'])
        self.assertEqual(980, topology.node[851]['latitude'])
        self.assertEqual('AS_NODE', topology.node[851]['type'])
        # 1478    716    230    212.11553455605272    0.7075412636166207    0.0011145252848059164    716    230    E_AS    U
        #assert_true((716, 230) in topology.edges())
        self.assertEquals(1478, topology.edge[716][230]['id'])
        self.assertAlmostEquals(212.11553455605272,
                                topology.edge[716][230]['length'], 0.01)


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_brite_router(self):
        pass


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_brite_bottomup(self):
        pass


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_brite_topdown(self):
        pass