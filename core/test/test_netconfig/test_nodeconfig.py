import unittest
from nose.tools import *
from fnss.netconfig.nodeconfig import *
from fnss.topologies.simplemodels import full_mesh_topology


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.topo = full_mesh_topology(100)
        cls.stack_1_name = 'stack_1'
        cls.stack_1_props = {'prop1': 'val11', 'prop2': 'val12'}
        cls.stack_2_name = 'stack_2'
        cls.stack_2_props = {'prop1': 'val12', 'prop2': 'val22'}
        cls.app_1_name = 'app_1'
        cls.app_1_props = {'prop1': 'val11', 'prop2': 'val12'}
        cls.app_2_name = 'app_2'
        cls.app_2_props = {'prop1': 'val12', 'prop2': 'val22'}
    
    def setUp(self):
        pass


    def tearDown(self):
        clear_stacks(self.topo)
        clear_applications(self.topo)

    def test_add_get_remove_stack(self):
        for v in self.topo.nodes():
            assert_is_none(get_stack(self.topo, v))
        add_stack(self.topo, 12, self.stack_1_name, self.stack_1_props)
        assert_equal(2, len(get_stack(self.topo, 12)))
        assert_is_none(get_stack(self.topo, 3))
        assert_equal(self.stack_1_name, get_stack(self.topo, 12)[0])
        assert_equal(self.stack_1_props, get_stack(self.topo, 12)[1])
        add_stack(self.topo, 12, self.stack_1_name, self.stack_2_props)
        assert_equal(self.stack_1_name, get_stack(self.topo, 12)[0])
        assert_equal(self.stack_2_props, get_stack(self.topo, 12)[1])
        add_stack(self.topo, 12, self.stack_2_name, self.stack_2_props)
        assert_equal(self.stack_2_name, get_stack(self.topo, 12)[0])
        assert_equal(self.stack_2_props, get_stack(self.topo, 12)[1])
        remove_stack(self.topo, 12)
        assert_is_none(get_stack(self.topo, 12))
        
    def test_clear_stacks(self):
        for v in self.topo.nodes():
            add_stack(self.topo, v, self.stack_1_name, self.stack_1_props)
        clear_stacks(self.topo)
        for v in self.topo.nodes():
            assert_is_none(get_stack(self.topo, v))
    
    def test_add_get_remoe_applications(self):
        for v in self.topo.nodes():
            assert_equal([], get_application_names(self.topo, v))
        add_application(self.topo, 10, self.app_1_name, self.app_1_props)
        assert_equal([self.app_1_name], get_application_names(self.topo, 10))
        assert_equal(self.app_1_props, get_application_properties(self.topo, 10, self.app_1_name))
        add_application(self.topo, 10, self.app_1_name, self.app_2_props)
        assert_equal([self.app_1_name], get_application_names(self.topo, 10))
        assert_equal(self.app_2_props, get_application_properties(self.topo, 10, self.app_1_name))
        add_application(self.topo, 10, self.app_2_name, self.app_2_props)
        assert_equal([self.app_1_name, self.app_2_name], get_application_names(self.topo, 10))
        assert_equal(self.app_2_props, get_application_properties(self.topo, 10, self.app_1_name))
        assert_equal(self.app_2_props, get_application_properties(self.topo, 10, self.app_2_name))
        remove_application(self.topo, 10, self.app_2_name)
        assert_equal([self.app_1_name], get_application_names(self.topo, 10))
        remove_application(self.topo, 10, self.app_1_name)
        assert_equal([], get_application_names(self.topo, 10))
        add_application(self.topo, 10, self.app_1_name, self.app_1_props)
        add_application(self.topo, 10, self.app_2_name, self.app_1_props)
        remove_application(self.topo, 10)
        assert_equal([], get_application_names(self.topo, 10))
        
    def test_clear_applications(self):
        for v in self.topo.nodes():
            add_application(self.topo, v, self.app_1_name, self.app_1_props)
            add_application(self.topo, v, self.app_2_name, self.app_2_props)
        clear_applications(self.topo)
        for v in self.topo.nodes():
            assert_equal([], get_application_names(self.topo, v))