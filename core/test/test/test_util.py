import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
import fnss.util as util


class TestSplitList(unittest.TestCase):

    def test_no_remainder(self):
        l = util.split_list([1, 2, 3, 4, 5, 6], 2)
        self.assertEqual(l, [[1, 2], [3, 4], [5, 6]])
        
    def test_remainder(self):
        l = util.split_list([1, 2, 3], 2)
        self.assertEqual(l, [[1, 2], [3]])


class TestGeographicalDistance(unittest.TestCase):
    
    def test_normal_case(self):
        d = util.geographical_distance(-30, -30, 30, 30)
        self.assertGreater(d, 0)
    
    def test_pole_node(self):
        d = util.geographical_distance(90, 30, 40, 90)
        self.assertGreater(d, 0)