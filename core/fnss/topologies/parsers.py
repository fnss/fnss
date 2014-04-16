"""
Provides functions to parse topologies from datasets or from outputs of
other generators.
"""
import re
import math

import networkx as nx

from fnss.topologies.topology import Topology, DirectedTopology
from fnss.util import geographical_distance


__all__ = [
    'parse_rocketfuel_isp_map',
    'parse_caida_as_relationships',
    'parse_inet',
    'parse_abilene',
    'parse_brite',
    'parse_topology_zoo',
    'parse_ashiip'
          ]


# Parser for RocketFuel ISP (router-level) maps .cch files
def parse_rocketfuel_isp_map(path):
    """
    Parse a network topology from RocketFuel ISP map file.
    
    Parameters
    ----------
    path : str
        The path of the file containing the RocketFuel map. It should have 
        extension .cch

    Returns
    -------
    topology : DirectedTopology
        The object containing the parsed topology.
    
    Notes
    -----
    The returned topology is always directed. If an undirected topology is
    desired, convert it using the DirectedTopology.to_undirected() method.
    
    Each node of the returned graph has the following attributes:
     * **type**: string
     * **location**: string (optional)
     * **address**: string 
     * **r**: int
     * **backbone**: boolean (optional)
        
    Each edge of the returned graph has the following attributes:
     * type : string, which can either be *internal* or *external*
     
    If the topology contains self-loops (links starting and ending in the same
    node) they are stripped from the topology.
    
    Raises
    ------
    ValueError
        If the provided file cannot be parsed correctly.
        
    Examples
    --------
    >>> import fnss
    >>> topology = fnss.parse_rocketfuel_isp_map('1221.r0.cch')
    """
    topology = DirectedTopology(type='rocket_fuel')
    comment_char = '#'
    
    for line in open(path, "r").readlines():
        if comment_char in line:
            # split on comment char, keep only the part before
            line, _ = line.split(comment_char, 1)
            line = line.strip()
        if len(line) > 0:
            #Parse line.
            if line.startswith("-"):
                # Case external node     
                # -euid =externaladdress rn
                try:
                    node = int(re.findall("-\d+", line)[0])
                    address = (re.findall("=\S+", line)[0])[1:]  # .strip("=")
                    r = int(re.findall("r\d$", line)[0][1:])  # .strip("r"))
                except IndexError:
                    raise ValueError('Invalid input file. Parsing failed '\
                                     'while trying to parse an external node')
                topology.add_node(node, type='external', address=address, r=r)
            else:
                # Case internal node
                # uid @loc [+] [bb] (num_neigh) [&ext] -> <nuid-1> <nuid-2> 
                # ... {-euid} ... =name[!] rn
                try:
                    node = int(re.findall("\d+", line)[0])
                    node_location = re.findall("@\S*", line)[0]
                    node_location = re.sub("[\+@]", "", node_location)
                    r = int(re.findall("r\d$", line)[0][1:])# .strip("r"))
                    address = (re.findall("=\S+", line)[0])[1:]  # .strip("=")
                except IndexError:
                    raise ValueError('Invalid input file. Parsing failed '\
                                     'while trying to parse an internal node')
                internal_links = re.findall("<(\d+)>", line)
                external_links = re.findall("{(-?\d+)}", line)
                backbone = True if len(re.findall("\sbb\s", line)) > 0 \
                           else False
                topology.add_node(node, type='internal', 
                                  location=node_location, 
                                  address=address, r=r, backbone=backbone)
                for link in internal_links:
                    link = int(link)
                    if node != link:
                        topology.add_edge(node, link, type='internal')
                for link in external_links:
                    link = int(link)
                    if node != link:
                        topology.add_edge(node, link, type='external')
    return topology


# Parser for CAIDA AS-relationships dataset
# Data from http://www.caida.org/data/active/as-relationships/
# http://as-rank.caida.org/data/
def parse_caida_as_relationships(path):
    """
    Parse a topology from the CAIDA AS relationships dataset
    
    Parameters
    ----------
    path : str
        The path to the CAIDA AS relationships file
    
    Returns
    -------
    topology : DirectedTopology
    
    Notes
    -----
    The node names of the returned topology are the the ASN of the of the AS 
    they represent and edges are annotated with the relationship between ASes 
    they connect. The relationship values can either be *customer*, *peer* or
    *sibling*.     
    """
    topology = DirectedTopology(type='caida_as_relationships')
    comment_char = '#'
    relationships_dict = {-1: 'customer', 0: 'peer', 2: 'sibling'}
    
    for line in open(path, "r").readlines():
        if comment_char in line:
            # split on comment char, keep only the part before
            line, _ = line.split(comment_char, 1)
            line = line.strip()
        if len(line) == 0:
            continue
        entry = line.split('|')
        try:
            from_as = int(entry[0])
            to_as = int(entry[1])
            relationship = relationships_dict[int(entry[2])]
        except (ValueError, IndexError, KeyError):
            raise ValueError('Invalid input file. Parsing failed while trying'\
                             ' to parse a line')
        if from_as != to_as:
            topology.add_edge(from_as, to_as, type=relationship)
    return topology


def parse_inet(path):
    """
    Parse a topology from an output file generated by the Inet topology
    generator
    
    Parameters
    ----------
    path : str
        The path to the Inet output file
        
    Returns
    -------
    topology : Topology
    
    Notes
    -----
    Each node of the returned topology object is labeled with *latitude* and
    *longitude* attributes. These attributes are not expressed in degrees but
    in Kilometers.
    """
    topology = Topology(type='inet', distance_unit='Km')
    lines = open(path, "r").readlines()
    sep = re.compile('[\s\t]')
    first_line = sep.split(lines[0].strip())
    try:
        n_nodes = int(first_line[0])
        n_links = int(first_line[1])
    except (ValueError, IndexError):
        raise ValueError('Invalid input file. '\
                         'Cannot parse the number of nodes and links')
    if len(lines) != 1 + n_nodes + n_links:
        raise ValueError('Invalid input file. '\
                         'It does not have as many lines as expected')
    i = 0
    for line in lines[1:]:
        entry = sep.split(line.strip())
        if i < n_nodes:
            i += 1
            try:
                node_id = int(entry[0])
                longitude = int(entry[1])
                latitude = int(entry[2])
            except (ValueError, IndexError):
                raise ValueError('Invalid input file. Parsing failed while '\
                                 'trying to parse a node')
            topology.add_node(node_id, latitude=latitude, longitude=longitude)
        else:
            try:
                u = int(entry[0])
                v = int(entry[1])
                weight = int(entry[2])
                x_u = topology.node[u]['longitude']
                y_u = topology.node[u]['latitude']
                x_v = topology.node[v]['longitude']
                y_v = topology.node[v]['latitude']
                length = float(math.sqrt((x_v - x_u)**2 + (y_v - y_u)**2))
            except (ValueError, IndexError):
                raise ValueError('Invalid input file. Parsing failed while '\
                                 'trying to parse a link')
            topology.add_edge(u, v, weight=weight, length=length)
    return topology


# Ignore external links
# Node parameters: city, latitude, longitude
# Link parameters: capacity, weight[, link_index, link_type]
def parse_abilene(topology_file, links_file=None):
    """
    Parse the Abilene topology.
    
    Parameters
    ----------
    topology_file : str
        The path of the Abilene topology file
    links_file : str, optional
        The path of the Abilene links file
    
    Returns
    -------
    topology : DirectedTopology
    """
    topology = DirectedTopology(type='abilene', 
                         capacity_unit='kbps', 
                         distance_unit='Km')
    comment_char = '#'
    link_type_dict = {0: 'internal', 1: 'inbound', 2: 'outbound'}
    line_type = None
    for line in open(topology_file, "r").readlines():
        if comment_char in line:
            # split on comment char, keep only the part before
            line, _ = line.split(comment_char, 1)
        line = line.strip()
        if len(line) > 0:
            if line == 'router' or line == 'link':
                line_type = line
                continue
            if line_type == 'router': 
                node_entry = line.split('\t')
                try:
                    name = node_entry[0]
                    city = node_entry[1]
                    latitude = float(node_entry[2])
                    longitude = float(node_entry[3])
                except (ValueError, IndexError):
                    raise ValueError('Invalid input file. Parsing failed '\
                                     'while trying to parse a router')
                topology.add_node(name, city=city, latitude=latitude, 
                           longitude=longitude)
            elif line_type == 'link':
                sep = re.compile('[\s\t]')
                link_entry = sep.split(line)
                try:
                    u = link_entry[0]
                    v = link_entry[1]
                    capacity = int(link_entry[2])
                    lon_u = topology.node[u]['longitude']
                    lat_u = topology.node[u]['latitude']
                    lon_v = topology.node[v]['longitude']
                    lat_v = topology.node[v]['latitude']
                    length = geographical_distance(lat_v, lon_v, lat_u, lon_u)
                    weight = int(link_entry[3])
                except (ValueError, IndexError):
                    raise ValueError('Invalid input file. Parsing failed '\
                                     'while trying to parse a link')
                topology.add_edge(u, v, capacity=capacity, 
                           weight=weight, length=length)
            else:
                raise ValueError('Invalid input file. Found a line that '\
                                 'I cannot interpret')
    if links_file:
        for line in open(links_file, "r").readlines():
            if comment_char in line:
                # split on comment char, keep only the part before
                line, _ = line.split(comment_char, 1)
            line = line.strip()
            if len(line) > 0:
                sep = re.compile('[\s\t]')
                link_entry = sep.split(line)
                try:
                    u, v = link_entry[0].split(',', 1)
                    if u == '*' or v == '*': # ignore external links
                        continue
                    link_index = int(link_entry[1])
                    link_type = link_type_dict[int(link_entry[2])]
                except (ValueError, IndexError):
                    raise ValueError('Invalid input file. '\
                                     'Parsing failed while trying to '\
                                     'parse a link from links_file')
                topology.edge[u][v]['link_index'] = link_index
                topology.edge[u][v]['link_type'] = link_type        
    return topology


def parse_brite(path, capacity_unit='Mbps', delay_unit='ms',
                distance_unit='Km', directed=True):
    """
    Parse a topology from an output file generated by the BRITE topology 
    generator
    
    Parameters
    ----------
    path : str
        The path to the BRITE output file    
    capacity_unit : str, optional
        The unit in which link capacity values are expresses in the BRITE file
    delay_unit : str, optional
        The unit in which link delay values are expresses in the BRITE file
    distance_unit : str, optional
        The unit in which node coordinates are expresses in the BRITE file
    directed : bool, optional
        If True, the topology is parsed as directed topology.
        
    Returns
    -------
    topology : Topology or DirectedTopology
    
    Notes
    -----
    Each node of the returned topology object is labeled with *latitude* and
    *longitude* attributes. These attributes are not expressed in degrees but
    in *distance_unit*.
    """
    # BRITE output format:
    # http://www.cs.bu.edu/brite/user_manual/node29.html
    topology = DirectedTopology() if directed else Topology()
    topology.graph = {'type':'brite', 'capacity_unit':capacity_unit, 
               'delay_unit':delay_unit, 'distance_unit': distance_unit}
    line_type = None
    for line in open(path, "r").readlines():
        if line.startswith('Nodes:'):
            line_type = 'node'
        elif line.startswith('Edges:'):
            line_type = 'edge'
        elif line[0].isdigit():
            elements = line.strip().split("\t")
            if line_type == 'node':
                # Parse node
                try:
                    node_id = int(elements[0])
                    longitude = float(elements[1])
                    latitude = float(elements[2])
                    #indegree = int(elements[3])
                    #outdegree = int(elements[4])
                    as_id = int(elements[5])
                    # Node type can be:
                    # AS-only: AS_NODE
                    # Router-only: RT_NODE
                    # Top-down: RT_NODE, RT_BORDER
                    # Bottom-up: RT_NODE
                    node_type = elements[6]
                except (ValueError, IndexError):
                    raise ValueError('Invalid input file. Parsing failed '\
                                     'while trying to parse a node')
                topology.add_node(node_id, latitude=latitude, 
                                  longitude=longitude, type=node_type)
                if as_id > 0:
                    topology.node[node_id]['AS'] = as_id
            elif line_type == 'edge':
                # Parse link
                try:
                    edge_id = int(elements[0])
                    from_node = int(elements[1])
                    to_node = int(elements[2])
                    length = float(elements[3])
                    delay = float(elements[4])
                    capacity = float(elements[5])
                    #from_as = elements[6]
                    #to_as = elements[7]
                    # Link type can be:
                    # AS-only: E_AS
                    # Router-only: E_RT
                    # Top-down: E_AS, E_RT
                    # bottom-up: E_RT
                    link_type = elements[8]
                except (ValueError, IndexError):
                    raise ValueError('Invalid input file. Parsing failed '\
                                     'while trying to parse a link')
                topology.add_edge(from_node, to_node, id=edge_id, 
                                  length=length, delay=delay, 
                                  capacity=capacity, type=link_type)
            else:
                continue
    return topology


def parse_topology_zoo(path):
    """
    Parse a topology from the Topology Zoo dataset.
    
    Parameters
    ----------
    path : str
        The path to the Topology Zoo file
    
    Returns
    -------
    topology : Topology or DirectedTopology
        The parsed topology.
    
    Notes
    -----
    If the parsed topology contains bundled links, i.e. multiple links between
    the same pair or nodes, the topology is parsed correctly but each bundle of
    links is represented as a single link whose capacity is the sum of the
    capacities of the links of the bundle (if capacity values were provided).
    The returned topology has a boolean attribute named *link_bundling* which
    is True if the topology contains at list one bundled link or False
    otherwise. If the topology contains bundled links, then each link has an
    additional boolean attribute named *bundle* which is True if that specific
    link was bundled in the original topology or False otherwise. 
    """
    def try_convert_int(value):
        """
        Try to convert a string to an int. If not possible, returns the given
        value unchanged 
        """
        if type(value) != int:
            try:
                value = int(value)
            except ValueError:
                pass
        return value
    if path.endswith('.gml'):
        topo_zoo_graph = nx.read_gml(path)
    elif path.endswith('.graphml'):
        topo_zoo_graph = nx.read_graphml(path)
    else:
        raise ValueError('Invalid input file format. It must either be a GML '\
                         'or GraphML file (with extensions .gml or .graphml)')
    topology = DirectedTopology() if topo_zoo_graph.is_directed() \
               else Topology()
    topology.graph['type'] = 'topology_zoo'
    topology.graph['distance_unit'] = 'Km'
    topology.graph['link_bundling'] = True if topo_zoo_graph.is_multigraph() \
                                      else False
    for tv in topo_zoo_graph.nodes_iter():
        v = try_convert_int(tv)
        topology.add_node(v)
        if 'label' in topo_zoo_graph.node[tv]:
            topology.node[v]['label'] = topo_zoo_graph.node[tv]['label']
        try:
            longitude = topo_zoo_graph.node[tv]['Longitude']
            latitude = topo_zoo_graph.node[tv]['Latitude']
            topology.node[v]['longitude'] = longitude
            topology.node[v]['latitude'] = latitude
        except KeyError:
            pass
    for tv, tu in topo_zoo_graph.edges_iter():
        v = try_convert_int(tv)
        u = try_convert_int(tu)
        if u == v:
            continue
        topology.add_edge(v, u)
        if 'Latitude' in topo_zoo_graph.node[tv] and \
                'Longitude' in topo_zoo_graph.node[tv] and \
                'Latitude' in topo_zoo_graph.node[tu] and \
                'Longitude' in topo_zoo_graph.node[tu]:
            lat_v = topo_zoo_graph.node[tv]['Latitude'] 
            lon_v = topo_zoo_graph.node[tv]['Longitude'] 
            lat_u = topo_zoo_graph.node[tu]['Latitude']  
            lon_u = topo_zoo_graph.node[tu]['Longitude']
            length = geographical_distance(lat_v, lon_v, lat_u, lon_u)
            topology.edge[v][u]['length'] = length
        if topo_zoo_graph.is_multigraph():
            edge = topo_zoo_graph.edge[tv][tu]
            if len(edge) == 1:
                topology.edge[v][u]['bundle'] = False
                if 'LinkSpeedRaw' in edge[0]:
                    topology.edge[v][u]['capacity'] = \
                            edge[0]['LinkSpeedRaw']
            else:
                topology.edge[v][u]['bundle'] = True
                capacity = 0
                for edge_attr in list(edge.values()):
                    if 'LinkSpeedRaw' in edge_attr:
                        capacity += edge_attr['LinkSpeedRaw']
                if capacity > 0:
                    topology.edge[v][u]['capacity'] = capacity
        else:
            if 'LinkSpeedRaw' in topo_zoo_graph.edge[tv][tu]:
                topology.edge[v][u]['capacity'] = \
                        topo_zoo_graph.edge[tv][tu]['LinkSpeedRaw']
    if len(nx.get_edge_attributes(topology, 'capacity')) > 0:
        topology.graph['capacity_unit'] = 'bps'
    return topology


def parse_ashiip(file_name):
    """
    Parse a topology from an output file generated by the aShiip topology 
    generator
    
    Parameters
    ----------
    path : str
        The path to the aShiip output file
    
    Returns
    -------
    topology : Topology
    """
    topology = Topology(type='ashiip')
    
    for line in open(file_name, "r").readlines():
        # There is no documented aShiip format but we assume that if the line
        # does not start with a number it is not part of the topology
        if line[0].isdigit():
            node_ids = re.findall("\d+", line)
            if len(node_ids) < 3:
                raise ValueError('Invalid input file. Parsing failed while '\
                                 'trying to parse a line')
            node = int(node_ids[0])
            level = int(node_ids[1])
            topology.add_node(node, level=level)
            for i in range(2, len(node_ids)):
                topology.add_edge(node, int(node_ids[i]))
    return topology
