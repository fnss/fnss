from os import environ, path
import unittest

import fnss

RES_DIR = environ['test.res.dir'] if 'test.res.dir' in environ else None
TMP_DIR = environ['test.tmp.dir'] if 'test.tmp.dir' in environ else None

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_to_from(self):
        f = path.join(TMP_DIR, 'jfed-tofrom.rspec')
        t_in = fnss.Topology()
        t_in.add_path([1, 2, 3, 4])
        fnss.to_jfed(t_in, f)
        t_out = fnss.from_jfed(f)
        self.assertEqual(t_in.number_of_nodes(), t_out.number_of_nodes())
        self.assertEqual(t_in.number_of_edges(), t_out.number_of_edges())
        self.assertEqual(set(dict(t_in.degree()).values()),
                         set(dict(t_out.degree()).values()))

    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_to_jfed(self):
        t = fnss.Topology()
        t.add_path([1, 2, 3, 4])
        fnss.to_jfed(t, path.join(TMP_DIR, 'jfed-to.rspec'))
        pass

    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_from_jfed(self):
        rspec = path.join(RES_DIR, 'jfed-success.rspec')
        t = fnss.from_jfed(rspec)
        self.assertTrue(len(t) > 0)
