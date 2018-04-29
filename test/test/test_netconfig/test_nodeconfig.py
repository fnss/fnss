import unittest

import fnss

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.topo = fnss.full_mesh_topology(100)
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
        fnss.clear_stacks(self.topo)
        fnss.clear_applications(self.topo)

    def test_add_stack_no_attr(self):
        fnss.add_stack(self.topo, 1, 's_name')
        self.assertEqual(fnss.get_stack(self.topo, 1, data=False), 's_name')
        self.assertEqual(fnss.get_stack(self.topo, 1, data=True), ('s_name', {}))

    def test_add_stack_attr_dict(self):
        fnss.add_stack(self.topo, 1, 's_name', {'att1': 'val1'})
        self.assertEqual(fnss.get_stack(self.topo, 1, data=False), 's_name')
        self.assertEqual(fnss.get_stack(self.topo, 1, data=True), ('s_name', {'att1': 'val1'}))

    def test_add_stack_kw_attr(self):
        fnss.add_stack(self.topo, 1, 's_name', att1='val1')
        self.assertEqual(fnss.get_stack(self.topo, 1, data=False), 's_name')
        self.assertEqual(fnss.get_stack(self.topo, 1, data=True), ('s_name', {'att1': 'val1'}))

    def test_add_stack_mixed_attr(self):
        fnss.add_stack(self.topo, 1, 's_name', {'att1': 'val1'}, att2='val2')
        self.assertEqual(fnss.get_stack(self.topo, 1, data=False), 's_name')
        self.assertEqual(fnss.get_stack(self.topo, 1, data=True), ('s_name', {'att1': 'val1', 'att2': 'val2'}))

    def test_add_get_remove_stack(self):
        for v in self.topo.nodes():
            self.assertIsNone(fnss.get_stack(self.topo, v))
        fnss.add_stack(self.topo, 12, self.stack_1_name, self.stack_1_props)
        self.assertEqual(2, len(fnss.get_stack(self.topo, 12)))
        self.assertIsNone(fnss.get_stack(self.topo, 3))
        self.assertEqual(self.stack_1_name, fnss.get_stack(self.topo, 12)[0])
        self.assertEqual(self.stack_1_props, fnss.get_stack(self.topo, 12)[1])
        fnss.add_stack(self.topo, 12, self.stack_1_name, self.stack_2_props)
        self.assertEqual(self.stack_1_name, fnss.get_stack(self.topo, 12)[0])
        self.assertEqual(self.stack_2_props, fnss.get_stack(self.topo, 12)[1])
        fnss.add_stack(self.topo, 12, self.stack_2_name, self.stack_2_props)
        self.assertEqual(self.stack_2_name, fnss.get_stack(self.topo, 12)[0])
        self.assertEqual(self.stack_2_props, fnss.get_stack(self.topo, 12)[1])
        fnss.remove_stack(self.topo, 12)
        self.assertIsNone(fnss.get_stack(self.topo, 12))

    def test_clear_stacks(self):
        for v in self.topo.nodes():
            fnss.add_stack(self.topo, v, self.stack_1_name, self.stack_1_props)
        fnss.clear_stacks(self.topo)
        for v in self.topo.nodes():
            self.assertIsNone(fnss.get_stack(self.topo, v))

    def test_add_get_remove_applications(self):
        for v in self.topo.nodes():
            self.assertEqual([], fnss.get_application_names(self.topo, v))
        fnss.add_application(self.topo, 10, self.app_1_name, self.app_1_props)
        self.assertEqual([self.app_1_name],
                         fnss.get_application_names(self.topo, 10))
        self.assertEqual(self.app_1_props,
                         fnss.get_application_properties(self.topo, 10,
                                                    self.app_1_name))
        fnss.add_application(self.topo, 10, self.app_1_name, self.app_2_props)
        self.assertEqual([self.app_1_name],
                         fnss.get_application_names(self.topo, 10))
        self.assertEqual(self.app_2_props,
                         fnss.get_application_properties(self.topo, 10,
                                                    self.app_1_name))
        fnss.add_application(self.topo, 10, self.app_2_name, self.app_2_props)
        self.assertEqual(set([self.app_1_name, self.app_2_name]),
                         set(fnss.get_application_names(self.topo, 10)))
        self.assertEqual(self.app_2_props,
                         fnss.get_application_properties(self.topo, 10,
                                                    self.app_1_name))
        self.assertEqual(self.app_2_props,
                         fnss.get_application_properties(self.topo, 10,
                                                    self.app_2_name))
        fnss.remove_application(self.topo, 10, self.app_2_name)
        self.assertEqual([self.app_1_name],
                         fnss.get_application_names(self.topo, 10))
        fnss.remove_application(self.topo, 10, self.app_1_name)
        self.assertEqual([], fnss.get_application_names(self.topo, 10))
        fnss.add_application(self.topo, 10, self.app_1_name, self.app_1_props)
        fnss.add_application(self.topo, 10, self.app_2_name, self.app_1_props)
        fnss.remove_application(self.topo, 10)
        self.assertEqual([], fnss.get_application_names(self.topo, 10))

    def test_clear_applications(self):
        for v in self.topo.nodes():
            fnss.add_application(self.topo, v,
                                 self.app_1_name, self.app_1_props)
            fnss.add_application(self.topo, v,
                                 self.app_2_name, self.app_2_props)
        fnss.clear_applications(self.topo)
        for v in self.topo.nodes():
            self.assertEqual([], fnss.get_application_names(self.topo, v))
