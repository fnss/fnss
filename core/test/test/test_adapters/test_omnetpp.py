from os import environ, path
import unittest

import fnss

TMP_DIR = environ['test.tmp.dir'] if 'test.tmp.dir' in environ else None

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_to_omnetpp_undirected(self):
        t = fnss.Topology()
        t.add_path([1, 2, 3, 4])
        fnss.set_capacities_constant(t, 10, 'Gbps')
        fnss.set_delays_constant(t, 2, 'us')
        fnss.set_buffer_sizes_constant(t, 20, 'packets')
        fnss.to_omnetpp(t, path.join(TMP_DIR, 'omnetpp-undir.ned'))

    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_to_omnetpp_directed(self):
        t = fnss.DirectedTopology()
        t.add_path([1, 2, 3, 4])
        fnss.set_capacities_constant(t, 10, 'Gbps')
        fnss.set_delays_constant(t, 2, 'us')
        fnss.set_buffer_sizes_constant(t, 20, 'packets')
        fnss.to_omnetpp(t, path.join(TMP_DIR, 'omnetpp-dir.ned'))
