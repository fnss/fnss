"""Basic functions and classes for operating on network topologies."""
import xml.etree.cElementTree as ET
import networkx as nx
import fnss.util as util


__all__ = [
    'Topology',
    'DirectedTopology',
    'od_pairs_from_topology',
    'fan_in_out_capacities',
    'rename_edge_attribute',
    'rename_node_attribute',
    'read_topology',
    'write_topology',
           ]


class BaseTopology(object):
    """Base class for generic topology. Provides utility methods for listing
    nodes and edge properties.
    """

    def capacities(self):
        """Return a dictionary of all link capacities, keyed by link

        Returns
        -------
        capacities : dict
            A dictionary of link capacity, keyed by link
        """
        return nx.get_edge_attributes(self, 'capacity')

    def delays(self):
        """
        Return a dictionary of all link delays, keyed by link

        Returns
        -------
        delays : dict
            A dictionary of link delays, keyed by link
        """
        return nx.get_edge_attributes(self, 'delay')

    def weights(self):
        """Return a dictionary of all link weights, keyed by link

        Returns
        -------
        weights : dict
            A dictionary of all link weights, keyed by link
        """
        return nx.get_edge_attributes(self, 'weight')

    def buffers(self):
        """Return a dictionary of all buffer sizes, keyed by interface

        Returns
        -------
        buffers : dict
            A dictionary of buffer sizes, keyed by interface. The interface is
            a tuple (u, v) which is the link to which the the interface is
            outputting
        """
        return nx.get_edge_attributes(self, 'buffer')

    def stacks(self):
        """Return a dictionary of all node stacks, keyed by node

        Returns
        -------
        stacks : dict
            A dictionary of all node stacks, keyed by node. Each node stack is
            a tuple (name, properties) where name is the stack name and
            properties is a the dictionary
        """
        return nx.get_node_attributes(self, 'stack')

    def applications(self):
        """Return a dictionary of all applications deployed, keyed by node

        Returns
        -------
        applications : dict
            A dictionary of all applications deployed, keyed by node.
        """
        return nx.get_node_attributes(self, 'application')


class Topology(nx.Graph, BaseTopology):
    """Base class for undirected topology"""

    def __init__(self, data=None, name="", **kwargs):
        """Initialize the topology

        Parameters
        ----------
        data : input graph
            Data to initialize the topology.  If data=None (default) an empty
            topology is created. The data can be an edge list, or any
            FNSS Topology or NetworkX graph object.  If the corresponding
            optional Python packages are installed the data can also be a NumPy
            matrix or 2d ndarray, a SciPy sparse matrix, or a PyGraphviz graph.
        name : string, optional
            An optional name for the graph. Default is ""
        **kwargs : keyword arguments, optional
            Attributes to add to graph as key=value pairs.
        """
        super(Topology, self).__init__(data, name=name, **kwargs)

    def copy(self):
        """Return a copy of the topology.

        Returns
        -------
        topology : Topology
            A copy of the topology.

        See Also
        --------
        to_directed: return a directed copy of the topology.

        Notes
        -----
        This makes a complete copy of the topology including all of the
        node or edge attributes.

        Examples
        --------
        >>> topo = Topology()
        >>> topo.add_path([0,1,2,3])
        >>> copied_topo = topo.copy()

        """
        return Topology(super(Topology, self).copy())

    def subgraph(self, nbunch):
        """Return the subgraph induced on nodes in nbunch.

        The induced subgraph of the graph contains the nodes in nbunch
        and the edges between those nodes.

        Parameters
        ----------
        nbunch : list, iterable
            A container of nodes which will be iterated through once.

        Returns
        -------
        topology : Topology
            A subgraph of the graph with the same edge attributes.

        Notes
        -----
        The graph, edge or node attributes just point to the original graph.
        So changes to the node or edge structure will not be reflected in
        the original graph while changes to the attributes will.

        To create a subgraph with its own copy of the edge/node attributes use:
        Topology(G.subgraph(nbunch))

        If edge attributes are containers, a deep copy can be obtained using:
        G.subgraph(nbunch).copy()

        For an inplace reduction of a graph to a subgraph you can remove nodes:
        G.remove_nodes_from([ n in G if n not in set(nbunch)])

        Examples
        --------
        >>> topo = Topology()
        >>> topo.add_path([0,1,2,3])
        >>> topo2 = topo.subgraph([0,1,2])
        >>> topo2.edges()
        [(0, 1), (1, 2)]
        """
        return Topology(super(Topology, self).subgraph(nbunch))

    def to_directed(self):
        """Return a directed representation of the topology.

        Returns
        -------
        topology : DirectedTopology
            A directed topology with the same name, same nodes, and with
            each edge (u,v,data) replaced by two directed edges
            (u,v,data) and (v,u,data).

        Notes
        -----
        This returns a 'deepcopy' of the edge, node, and
        graph attributes which attempts to completely copy
        all of the data and references.

        This is in contrast to the similar D=DirectedTopology(G) which returns
        a shallow copy of the data.

        See the Python copy module for more information on shallow
        and deep copies, http://docs.python.org/library/copy.html.

        Examples
        --------
        >>> topo = Topology()
        >>> topo.add_path([0,1])
        >>> topo2 = topo.to_directed()
        >>> topo2.edges()
        [(0, 1), (1, 0)]

        If already directed, return a (deep) copy

        >>> topo = DirectedTopology()
        >>> topo.add_path([0,1])
        >>> topo2 = topo.to_directed()
        >>> topo2.edges()
        [(0, 1)]
        """
        return DirectedTopology(super(Topology, self).to_directed())

    def to_undirected(self):
        """Return an undirected copy of the topology.

        Returns
        -------
        topology : Topology
            A undirected copy of the topology.

        See Also
        --------
        copy, add_edge, add_edges_from

        Notes
        -----
        This returns a 'deepcopy' of the edge, node, and
        graph attributes which attempts to completely copy
        all of the data and references.

        This is in contrast to the similar G=Topology(D) which returns a
        shallow copy of the data.

        See the Python copy module for more information on shallow
        and deep copies, http://docs.python.org/library/copy.html.

        Examples
        --------
        >>> topo = Topology()   # or MultiGraph, etc
        >>> topo.add_path([0,1])
        >>> topo2 = topo.to_directed()
        >>> topo2.edges()
        [(0, 1), (1, 0)]
        >>> topo3 = topo2.to_undirected()
        >>> topo3.edges()
        [(0, 1)]
        """
        return Topology(super(Topology, self).to_undirected())


class DirectedTopology(nx.DiGraph, BaseTopology):
    """Base class for directed topology"""

    def __init__(self, data=None, name="", **kwargs):
        """Initialize the topology

        Parameters
        ----------
        data : input graph
            Data to initialize the topology.  If data=None (default) an empty
            topology is created. The data can be an edge list, or any
            FNSS Topology or NetworkX graph object.  If the corresponding
            optional Python packages are installed the data can also be a NumPy
            matrix or 2d ndarray, a SciPy sparse matrix, or a PyGraphviz graph.
        name : string, optional
            An optional name for the graph. Default is ""
        **kwargs : keyword arguments, optional
            Attributes to add to graph as key=value pairs.
        """
        super(DirectedTopology, self).__init__(data, name=name, **kwargs)

    def copy(self):
        """Return a copy of the topology.

        Returns
        -------
        topology : DirectedTopology
            A copy of the topology.

        See Also
        --------
        to_undirected: return a undirected copy of the topology.

        Notes
        -----
        This makes a complete copy of the topology including all of the
        node or edge attributes.

        Examples
        --------
        >>> topo = DirectedTopology()
        >>> topo.add_path([0,1,2,3])
        >>> copied_topo = topo.copy()
        """
        return DirectedTopology(super(DirectedTopology, self).copy())

    def subgraph(self, nbunch):
        """Return the subgraph induced on nodes in nbunch.

        The induced subgraph of the graph contains the nodes in nbunch
        and the edges between those nodes.

        Parameters
        ----------
        nbunch : list, iterable
            A container of nodes which will be iterated through once.

        Returns
        -------
        topology : DirectedTopology
            A subgraph of the graph with the same edge attributes.

        Notes
        -----
        The graph, edge or node attributes just point to the original graph.
        So changes to the node or edge structure will not be reflected in
        the original graph while changes to the attributes will.

        To create a subgraph with its own copy of the edge/node attributes use:
        Topology(G.subgraph(nbunch))

        If edge attributes are containers, a deep copy can be obtained using:
        G.subgraph(nbunch).copy()

        For an inplace reduction of a graph to a subgraph you can remove nodes:
        G.remove_nodes_from([ n in G if n not in set(nbunch)])

        Examples
        --------
        >>> topo = Topology()
        >>> topo.add_path([0,1,2,3])
        >>> topo2 = topo.subgraph([0,1,2])
        >>> topo2.edges()
        [(0, 1), (1, 2)]
        """
        return DirectedTopology(super(DirectedTopology, self).subgraph(nbunch))

    def to_directed(self):
        """Return a directed representation of the topology.

        Returns
        -------
        topology : DirectedTopology
            A directed topology with the same name, same nodes, and with
            each edge (u,v,data) replaced by two directed edges
            (u,v,data) and (v,u,data).

        Notes
        -----
        This returns a 'deepcopy' of the edge, node, and
        graph attributes which attempts to completely copy
        all of the data and references.

        This is in contrast to the similar D=DirectedTopology(G) which returns
        a shallow copy of the data.

        See the Python copy module for more information on shallow
        and deep copies, http://docs.python.org/library/copy.html.

        Examples
        --------
        >>> topo = Topology()
        >>> topo.add_path([0,1])
        >>> topo2 = topo.to_directed()
        >>> topo2.edges()
        [(0, 1), (1, 0)]

        If already directed, return a (deep) copy

        >>> topo = DirectedTopology()
        >>> topo.add_path([0,1])
        >>> topo2 = topo.to_directed()
        >>> topo2.edges()
        [(0, 1)]
        """
        return DirectedTopology(super(DirectedTopology, self).to_directed())

    def to_undirected(self):
        """Return an undirected copy of the topology.

        Returns
        -------
        topology : Topology
            A undirected copy of the topology.

        See Also
        --------
        copy, add_edge, add_edges_from

        Notes
        -----
        This returns a 'deepcopy' of the edge, node, and
        graph attributes which attempts to completely copy
        all of the data and references.

        This is in contrast to the similar G=Topology(D) which returns a
        shallow copy of the data.

        See the Python copy module for more information on shallow
        and deep copies, http://docs.python.org/library/copy.html.

        Examples
        --------
        >>> topo = Topology()   # or MultiGraph, etc
        >>> topo.add_path([0,1])
        >>> topo2 = topo.to_directed()
        >>> topo2.edges()
        [(0, 1), (1, 0)]
        >>> topo3 = topo2.to_undirected()
        >>> topo3.edges()
        [(0, 1)]
        """
        return Topology(super(DirectedTopology, self).to_undirected())


def od_pairs_from_topology(topology):
    """Calculate all possible origin-destination pairs of the topology.
    This function does not simply calculate all possible pairs of the topology
    nodes. Instead, it only returns pairs of nodes connected by at least
    a path.

    Parameters
    ----------
    topology : Topology or DirectedTopology
        The topology whose OD pairs are calculated

    Returns
    -------
    od_pair : list
        List containing all origin destination tuples.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.ring_topology(3)
    >>> fnss.od_pairs_from_topology(topology)
    [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    """
    if topology.is_directed():
        routes = dict(nx.all_pairs_shortest_path_length(topology))
        return [(o, d) for o in routes for d in routes[o] if o != d]
    else:
        conn_comp = nx.connected_components(topology)
        return [(o, d) for G in conn_comp for o in G for d in G if o != d]


def fan_in_out_capacities(topology):
    """Calculate fan-in and fan-out capacities for all nodes of the topology.

    The fan-in capacity of a node is the sum of capacities of all incoming
    links, while the fan-out capacity is the sum of capacities of all outgoing
    links.

    Parameters
    ----------
    topology : Topology
        The topology object whose fan-in and fan-out capacities are calculated.
        This topology must be annotated with link capacities.

    Returns
    -------
    fan_in_out_capacities : tuple (fan_in, fan_out)
        A tuple of two dictionaries, representing, respectively the fan-in and
        fan-out capacities keyed by node.

    Notes
    -----
    This function works correctly for both directed and undirected topologies.
    If the topology is undirected, the returned dictionaries of fan-in and
    fan-out capacities are identical.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.star_topology(3)
    >>> fnss.set_capacities_constant(topology, 10, 'Mbps')
    >>> in_cap, out_cap = fnss.fan_in_out_capacities(topology)
    >>> in_cap
    {0: 30, 1: 10, 2: 10, 3: 10}
    >>> out_cap
    {0: 30, 1: 10, 2: 10, 3: 10}
    """
    if not topology.is_directed():
        topology = topology.to_directed()
    fan_in = {}
    fan_out = {}
    for node in topology.nodes():
        node_fan_in = 0
        node_fan_out = 0
        for predecessor in topology.predecessors(node):
            node_fan_in += topology.adj[predecessor][node]['capacity']
        for successor in topology.successors(node):
            node_fan_out += topology.adj[node][successor]['capacity']
        fan_in[node] = node_fan_in
        fan_out[node] = node_fan_out
    return fan_in, fan_out


def rename_edge_attribute(topology, old_attr, new_attr):
    """Rename all edges attributes with a specific name to a new name

    Parameters
    ----------
    topology : Topology
        The topology object
    old_attr : any hashable type
        Old attribute name
    new_attr : any hashable type
        New attribute name

    Example
    -------
    >>> import fnss
    >>> topo = fnss.Topology()
    >>> topo.add_edge(1, 2, cost=1)
    >>> topo.add_edge(2, 3, cost=2)
    >>> topo.edges(data=True)
    [(1, 2, {'cost': 1}), (2, 3, {'cost': 2})]
    >>> fnss.rename_edge_attribute(topo, 'cost', 'weight')
    >>> topo.edges(data=True)
    [(1, 2, {'weight': 1}), (2, 3, {'weight': 2})]
    """
    for u, v in topology.edges():
        if old_attr in topology.adj[u][v]:
            topology.adj[u][v][new_attr] = topology.edge[u][v][old_attr]
            del topology.adj[u][v][old_attr]


def rename_node_attribute(topology, old_attr, new_attr):
    """Rename all nodes attributes with a specific name to a new name

    Parameters
    ----------
    topology : Topology
        The topology object
    old_attr : any hashable type
        Old attribute name
    new_attr : any hashable type
        New attribute name

    Example
    -------
    >>> import fnss
    >>> topo = fnss.Topology()
    >>> topo.add_node(1, pos=(0, 0))
    >>> topo.add_node(2, pos=(1, 1))
    >>> topo.nodes(data=True)
    [(1, {'pos': (0, 0)}), (2, {'pos': (1, 1)})]
    >>> fnss.rename_edge_attribute(topo, 'pos', 'coordinates')
    >>> topo.edges(data=True)
    [(1, {'coordinates': (0, 0)}), (2, {'coordinates': (1, 1)})]
    """
    for v in topology.nodes():
        if old_attr in topology.adj[v]:
            topology.node[v][new_attr] = topology.node[v][old_attr]
            del topology.node[v][old_attr]


def read_topology(path, encoding='utf-8'):
    """Read a topology from an XML file and returns either a Topology or a
    DirectedTopology object

    Parameters
    ----------
    path : str
        The path of the topology XML file to parse
    encoding : str, optional
        The encoding of the file

    Returns
    -------
    topology: Topology or DirectedTopology
        The parsed topology
    """
    tree = ET.parse(path)
    head = tree.getroot()
    topology = Topology() if head.attrib['linkdefault'] == 'undirected' \
                   else DirectedTopology()
    for prop in head.findall('property'):
        name = prop.attrib['name']
        value = util.xml_cast_type(prop.attrib['type'], prop.text)
        topology.graph[name] = value
    for node in head.findall('node'):
        v = util.xml_cast_type(node.attrib['id.type'], node.attrib['id'])
        topology.add_node(v)
        for prop in node.findall('property'):
            name = prop.attrib['name']
            value = util.xml_cast_type(prop.attrib['type'], prop.text)
            topology.node[v][name] = value
        if len(node.findall('stack')) > 0:
            if len(node.findall('stack')) > 1:
                raise ET.ParseError('Invalid topology. ' \
                                    'A node has more than one stack.')
            stack = node.findall('stack')[0]
            stack_name = util.xml_cast_type(stack.attrib['name.type'],
                                        stack.attrib['name'])
            stack_props = {}
            for prop in stack.findall('property'):
                name = prop.attrib['name']
                value = util.xml_cast_type(prop.attrib['type'], prop.text)
                stack_props[name] = value
            topology.node[v]['stack'] = (stack_name, stack_props)
        if len(node.findall('application')) > 0:
            topology.node[v]['application'] = {}
            for application in node.findall('application'):
                app_name = util.xml_cast_type(application.attrib['name.type'],
                                          application.attrib['name'])
                app_props = {}
                for prop in application.findall('property'):
                    name = prop.attrib['name']
                    value = util.xml_cast_type(prop.attrib['type'], prop.text)
                    app_props[name] = value
                topology.node[v]['application'][app_name] = app_props
    for edge in head.findall('link'):
        u = util.xml_cast_type(edge.find('from').attrib['type'],
                           edge.find('from').text)
        v = util.xml_cast_type(edge.find('to').attrib['type'],
                           edge.find('to').text)
        topology.add_edge(u, v)
        for prop in edge.findall('property'):
            name = prop.attrib['name']
            value = util.xml_cast_type(prop.attrib['type'], prop.text)
            topology.adj[u][v][name] = value
    return topology


def write_topology(topology, path, encoding='utf-8', prettyprint=True):
    """Write a topology object on an XML file

    Parameters
    ----------
    topology : Topology
        The topology object to write
    path : str
        The file ob which the topology will be written
    encoding : str, optional
        The encoding of the target file
    prettyprint : bool, optional
        Indent the XML code in the output file
    """
    head = ET.Element('topology')
    head.attrib['linkdefault'] = 'directed' if topology.is_directed() \
                                            else 'undirected'
    for name, value in topology.graph.items():
        prop = ET.SubElement(head, 'property')
        prop.attrib['name'] = name
        prop.attrib['type'] = util.xml_type(value)
        prop.text = str(value)
    for v in topology.nodes():
        node = ET.SubElement(head, 'node')
        node.attrib['id'] = str(v)
        node.attrib['id.type'] = util.xml_type(v)
        for name, value in topology.node[v].items():
            if name is 'stack':
                stack_name, stack_props = topology.node[v]['stack']
                stack = ET.SubElement(node, 'stack')
                stack.attrib['name'] = stack_name
                stack.attrib['name.type'] = util.xml_type(stack_name)
                for prop_name, prop_value in stack_props.items():
                    prop = ET.SubElement(stack, 'property')
                    prop.attrib['name'] = prop_name
                    prop.attrib['type'] = util.xml_type(prop_value)
                    prop.text = str(prop_value)
            elif name is 'application':
                for application_name, application_props in \
                            topology.node[v]['application'].items():
                    application = ET.SubElement(node, 'application')
                    application.attrib['name'] = application_name
                    application.attrib['name.type'] = \
                            util.xml_type(application_name)
                    for prop_name, prop_value in application_props.items():
                        prop = ET.SubElement(application, 'property')
                        prop.attrib['name'] = prop_name
                        prop.attrib['type'] = util.xml_type(prop_value)
                        prop.text = str(prop_value)
            else:
                prop = ET.SubElement(node, 'property')
                prop.attrib['name'] = name
                prop.attrib['type'] = util.xml_type(value)
                prop.text = str(value)
    for u, v in topology.edges():
        link = ET.SubElement(head, 'link')
        from_node = ET.SubElement(link, 'from')
        from_node.attrib['type'] = util.xml_type(u)
        from_node.text = str(u)
        to_node = ET.SubElement(link, 'to')
        to_node.attrib['type'] = util.xml_type(v)
        to_node.text = str(v)
        for name, value in topology.adj[u][v].items():
            prop = ET.SubElement(link, 'property')
            prop.attrib['name'] = name
            prop.attrib['type'] = util.xml_type(value)
            prop.text = str(value)
    if prettyprint:
        util.xml_indent(head)
    ET.ElementTree(head).write(path, encoding=encoding)
