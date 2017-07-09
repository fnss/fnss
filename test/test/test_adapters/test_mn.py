import unittest

import fnss
from fnss.util import package_available

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipUnless(package_available('mininet'), 'Requires Mininet')
    def test_to_mininet(self):
        t = fnss.Topology()
        t.add_path([1, 2, 3, 4])
        for n in (1, 4):
            t.node[n]['type'] = 'host'
        for n in (2, 3):
            t.node[n]['type'] = 'switch'
        fnss.set_capacities_constant(t, 10, 'Mbps')
        fnss.set_delays_constant(t, 10, 'ms')
        mn_topo = fnss.to_mininet(t, relabel_nodes=False)
        self.assertIsNotNone(mn_topo)
        hosts = mn_topo.hosts()
        switches = mn_topo.switches()
        for h in '1', '4':
            self.assertIn(h, hosts)
        for s in '2', '3':
            self.assertIn(s, switches)
        mn_topo = fnss.to_mininet(t, relabel_nodes=True)
        # Relabeling should be:
        # 1 -> h1
        # 2 -> s1
        # 3 -> s2
        # 4 -> h2
        self.assertIsNotNone(mn_topo)
        hosts = mn_topo.hosts()
        switches = mn_topo.switches()
        for h in 'h1', 'h2':
            self.assertIn(h, hosts)
        for s in 's1', 's2':
            self.assertIn(s, switches)

    @unittest.skipUnless(package_available('mininet'), 'Requires Mininet')
    def test_from_mininet(self):
        try:
            from mininet.topo import Topo
        except ImportError:
            raise ImportError('You must have Mininet installed to run this test case')
        t = Topo()
        t.addHost("h1")
        t.addHost("h4")
        t.addSwitch("s2")
        t.addSwitch("s3")
        t.addLink("h1", "s2")
        t.addLink("s2", "s3")
        t.addLink("s3", "h4")
        fnss_topo = fnss.from_mininet(t)
        self.assertIsNotNone(fnss_topo)
        for h in "h1", "h4":
            self.assertEqual(fnss_topo.node[h]['type'], 'host')
        for s in "s2", "s3":
            self.assertEqual(fnss_topo.node[s]['type'], 'switch')
