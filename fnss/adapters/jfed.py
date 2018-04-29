"""Adapter for jFed

Provides function to convert an FNSS Topology object into a jFed
rspec file and viceversa.

`jFed <http://jfed.iminds.be/>_` is a Java-based framework to support the
integration of federated testbed, developed by
`iMinds <http://www.iminds.be/>_` in the contex of the
`Fed4FIRE <http://www.fed4fire.eu/>_` project funded by the Framework
Programme 7 (FP7) of the European Union.
"""
from __future__ import division
import xml.etree.cElementTree as ET

import networkx as nx

from fnss import Topology, get_delays, get_capacities
import fnss.util as util
import fnss.units as units


__all__ = ['to_jfed', 'from_jfed']


def to_jfed(topology, path, testbed="wall1.ilabt.iminds.be", encoding="utf-8", prettyprint=True):
    """Convert a topology object into an RSPEC file for jFed

    Parameters
    ----------
    topology : Topology
        The topology object
    path : str
        The file to which the RSPEC will be written
    testbed : str, optional
        URI of the testbed to use
    encoding : str, optional
        The encoding of the target file
    prettyprint : bool, optional
        Indent the XML code in the output file

    Notes
    -----
    It currently supports only undirected topologies, if a topology is directed
    it is converted to undirected
    """
    if topology.is_directed():
        topology = topology.to_undirected()
    topology = nx.convert_node_labels_to_integers(topology)

    if 'capacity_unit' in topology.graph:
        capacity_norm = units.capacity_units[topology.graph['capacity_unit']] / units.capacity_units['Kbps']
    if 'delay_unit' in topology.graph:
        delay_norm = units.time_units[topology.graph['delay_unit']] / units.time_units['ms']
    delays = get_delays(topology)
    capacities = get_capacities(topology)
    # Node positions (randomly generated)
    pos = nx.random_layout(topology)
    # Create mapping between links and interface IDs
    if_names = {}
    for v in topology.adj:
        next_hops = sorted(topology.adj[v].keys())
        if_names[v] = {next_hop: i for i, next_hop in enumerate(next_hops)}
    head = ET.Element('rspec')
    head.attrib["generated_by"] = "FNSS"
    head.attrib['xsi:schemaLocation'] = "http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd"
    head.attrib['xmlns'] = "http://www.geni.net/resources/rspec/3"
    head.attrib["xmlns:jFed"] = "http://jfed.iminds.be/rspec/ext/jfed/1"
    head.attrib["xmlns:jFedBonfire"] = "http://jfed.iminds.be/rspec/ext/jfed-bonfire/1"
    head.attrib["xmlns:delay"] = "http://www.protogeni.net/resources/rspec/ext/delay/1"
    head.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
    # Iterate over nodes
    for v in topology.nodes():
        node = ET.SubElement(head, 'node')
        node.attrib['client_id'] = "node%s" % str(v)
        node.attrib['component_manager_id'] = "urn:publicid:IDN+%s+authority+cm" % testbed
        node.attrib["exclusive"] = "true"
        sliver_type = ET.SubElement(node, 'sliver_type')
        sliver_type.attrib['name'] = topology.node[v]['sliver_type'] if 'sliver_type' in topology.node[v] else 'raw-pc'
        location = ET.SubElement(node, 'jFed:location')
        x, y = pos[v]
        location.attrib['x'] = str(1000 * x)
        location.attrib['y'] = str(500 * y)
        for if_name in if_names[v].values():
            interface = ET.SubElement(node, 'interface')
            interface.attrib['client_id'] = "node%s:if%s" % (str(v), str(if_name))
    # The convention in jFed is to identify links with "linkX" where X is an
    # integer but making sure that links and nodes have different integers
    link_id = topology.number_of_nodes() - 1
    for u, v in topology.edges():
        link_id += 1
        link = ET.SubElement(head, 'link')
        link.attrib['client_id'] = "link%s" % str(link_id)
        component_manager = ET.SubElement(link, 'component_manager')
        component_manager.attrib['name'] = "urn:publicid:IDN+%s+authority+cm" % testbed
        u_if = "node%s:if%s" % (str(u), str(if_names[u][v]))
        v_if = "node%s:if%s" % (str(v), str(if_names[v][u]))
        for source, dest in ((u_if, v_if), (v_if, u_if)):
            prop = ET.SubElement(link, 'property')
            prop.attrib["source_id"] = source
            prop.attrib["dest_id"] = dest
            if (u, v) in delays:
                prop.attrib['latency'] = str(delay_norm * delays[(u, v)])
            if (u, v) in capacities:
                prop.attrib['capacity'] = str(capacity_norm * capacities[(u, v)])
            interface_ref = ET.SubElement(link, 'interface_ref')
            interface_ref.attrib['client_id'] = source
    if prettyprint:
        util.xml_indent(head)
    ET.ElementTree(head).write(path, encoding=encoding)


def from_jfed(path):
    """Read a jFed RSPEC file and returns an FNSS topology modelling the
    network topology of the jFed experiment specification.

    Parameters
    ----------
    path : str
        The path of the jFed RSPEC file to parse

    Returns
    -------
    topology: Topology
        The parsed topology

    Notes
    -----
    This function does not support directed topologies and unidirectional links

    It is possible in jFed to create multipoint links (links with more than 2
    endpoints). Such types of link cannot be modelled in FNSS. Therefore, any
    attempt to convert an RSPEC with such links will fail.
    """
    # This implementation could be improved by using SOAP libraries, but it
    # would require to add another dependency to the project.
    # The current implementation, although not really elegant, works fine
    tree = ET.parse(path)
    head = tree.getroot()
    xmlns = "http://www.geni.net/resources/rspec/3"
    topology = Topology()
    # Flags to indicate whether the parsed topology is annotated with
    # capacities and delays
    has_delays = False
    has_capacities = False
    # Dict mapping interface name to the node it belongs to
    if_map = {}
    # Iterate over nodes
    for node in head.findall('{%s}node' % xmlns):
        client_id = node.attrib['client_id']
        component_manager_id = node.attrib['component_manager_id']
        exclusive = bool(node.attrib['exclusive'])
        for interface in node.findall('{%s}interface' % xmlns):
            if_id = interface.attrib['client_id']
            if_map[if_id] = client_id
        topology.add_node(client_id,
                          component_manager_id=component_manager_id,
                          exclusive=exclusive)
    # Iterate over links
    for edge in head.findall('{%s}link' % xmlns):
        client_id = edge.attrib['client_id']
        component_manager = edge.find('{%s}component_manager' % xmlns).attrib['name']
        interfaces = edge.findall('{%s}interface_ref' % xmlns)
        # A link may connect more than two nodes. These links cannot be
        # represented in an FNSS Topology.
        # This statement also encompasses the potential case of one interface
        # only that should not happen if the file is correctly formatted.
        if len(interfaces) != 2:
            raise ValueError("Link %s is not a point-to-point link but a shared "
                             "medium connecting %d interfaces. These links are "
                             "not supported. Change your topology and try again"
                             % (client_id, len(interfaces)))
        u = if_map[interfaces[0].attrib['client_id']]
        v = if_map[interfaces[1].attrib['client_id']]
        edge_attr = dict(component_manager=component_manager,
                         client_id=client_id)
        # There are normally two property tags per edge. We only parse one
        # because should have same attributes if links are bidirectional.
        # This function does not support unidirectional links
        prop = edge.find('{%s}property' % xmlns)
        if prop:
            if 'capacity' in prop.attrib:
                edge_attr['capacity'] = prop.attrib['capacity']
                has_capacities = True
            if 'latency' in prop.attrib:
                edge_attr['delay'] = prop.attrib['latency']
                has_delays = True
        topology.add_edge(u, v, **edge_attr)
    # Set capacity and delay units
    if has_capacities:
        topology.graph['capacity_unit'] = 'kbps'
    if has_delays:
        topology.graph['delay_unit'] = 'ms'
    return topology
