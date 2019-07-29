"""Basic utility functions"""
from __future__ import division
import ast
import random
from math import pi, sqrt, sin, cos, asin

from fnss.units import EARTH_RADIUS

__all__ = [
    'split_list',
    'random_from_pdf',
    'map_func',
    'xml_cast_type',
    'xml_type',
    'xml_indent',
    'geographical_distance',
    'package_available',
    'extend_link_tuple_to_all_parallel',
    'extend_link_list_to_all_parallel',
    'find_link_key_with_smallest_weight',
    'find_all_link_keys_with_smallest_weight',
    'find_link_between_nodes_with_smallest_weight',
          ]


def split_list(l, size):
    """Split a list into evenly sized chunks

    Parameters
    ----------
    l : list
        The list to split
    size : n
        The size of each chunk

    Returns
    -------
    A list of sub-lists

    Examples
    --------
    >>> from fnss.util import split_list
    >>> split_list([1, 2, 3, 4, 5, 6], 2)
    [[1, 2], [3, 4], [5, 6]]
    """
    return [l[i: i + size] for i in range(0, len(l), size)]


def random_from_pdf(pdf, seed=None):
    """Return a random value according to a given probability density function.

    Parameters
    ----------
    pdf : dict
        Dictionary mapping values of the random variable and probability of
        occurrence. The sum of all dictionary values must be 1.
    seed : int, optional
        The seed to be used

    Returns
    -------
    key : key of pdf
        A randomly selected key from the keyset of the *pdf* parameter

    Examples
    --------
    >>> pdf = {100: 0.5, 200: 0.5}
    >>> random_from_pdf(pdf)
    100 # random
    """
    # validate input parameters
    if not isinstance(pdf, dict):
        raise ValueError('The parameter pdf must be a dictionary')
    if abs(sum(pdf.values()) - 1) > 0.0001:
        raise ValueError('The sum of all probabilities must be equal to 1')
    if seed is not None:
        random.seed(seed)
    r = random.random()
    w = 0.0
    for key, value in pdf.items():
        w += value
        if r < w:
            return key


def map_func(x):
    """Execute a function with given arguments, both of them passed as an argument

    This function is used to execute map operations on a function taking an
    arbitrary number of arguments

    Parameters
    ----------
    x : tuple (func, args)
        A tuple where the first argument is the function to execute and the
        second argument is a tuple of arguments
    """
    func, args = x
    return func(*args)


def xml_cast_type(type_attrib, val):
    """Cast a value read to an XML to an appropriate Python type

    Parameters
    ----------
    type_attrib : str
        The type of the value as specified in the XML file
    val : str
        The value to cast

    Returns
    -------
    cast_val : any type
        The val argument cast to a given type
    """
    if type_attrib == 'int':
        return int(val)
    elif type_attrib == 'float':
        return float(val)
    elif type_attrib == 'boolean':
        if val == 'True':
            return True
        else:
            return False
    elif type_attrib in ('tuple', 'list', 'dict'):
        return ast.literal_eval(val)
    else:
        return val


def xml_type(val):
    """Return a type string for writing to an XML file.

    Parameters
    ----------
    val : any type
        The value

    Returns
    -------
    type : str
        The type of the value to insert in the XML file
    """
    try:
        return {str:   'string',
                int:   'int',
                bool:  'boolean',
                float: 'float',
                dict:  'dict',
                list:  'list',
                tuple: 'tuple'
        }[type(val)]
    except KeyError:
        return 'string'


def xml_indent(elem, level=0):
    """Indent the elements of the XML tree

    Parameters
    ----------
    elem : xml.etree.Element object
        XML Element to indent
    level : int, optional
        The starting indentation level
    """
    i = "\n" + (level * "  ")
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            xml_indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def package_available(pkg):
    """Test whether a package is available or not

    Parameters
    ----------
    pkg : string
        Name of the package to look for

    Returns
    -------
    pkg_available : bool
        *True* if the package is available, *False* otherwise
    """
    try:
        exec('import %s' % pkg)
    except ImportError:
        return False
    else:
        return True


def geographical_distance(lat_u, lon_u, lat_v, lon_v):
    """Return geographical distance along the Earth surface between two points
    *u* and *v*

    This distance is computed using the Haversine formula.

    Parameters
    ----------
    lat_u : float
        Latitude of point *u* in degrees
    lon_u : float
        Longitude of point *u* in degrees
    lat_v : float
        Latitude of point *v* in degrees
    lon_v : float
        Longitude of point *v* in degrees

    Returns
    -------
    d : float
        The distance between *u* and *v*
    """
    lat_u = (pi / 180) * lat_u
    lon_u = (pi / 180) * lon_u
    lat_v = (pi / 180) * lat_v
    lon_v = (pi / 180) * lon_v
    return 2 * EARTH_RADIUS * asin(sqrt(sin((lat_u - lat_v) / 2) ** 2 +
                                    cos(lat_v) * cos(lat_u)
                                    * sin((lon_u - lon_v) / 2) ** 2))


def extend_link_tuple_to_all_parallel(topology, link):
    """Convert (u,v) link tuples to [(u,v,key),...] list including all possible keys"""
    if len(link) == 3:
        return [link]
    else:
        u, v = link
        return [link + (key,) for key in topology.adj[u][v]]


def extend_link_list_to_all_parallel(topology, links):
    """Convert [(u,v),...] links to [(u,v,key),...] list including all possible keys for given (u,v) pair"""
    return [ext_link
            for link in links
            for ext_link in extend_link_tuple_to_all_parallel(topology, link)]


def find_link_key_with_smallest_weight(topology, u, v, weight_attr):
    """Return a single ((u,v,key), weight) for (u,v) links with the smallest `weight_attr` if exists,
    otherwise (None, None)
    """
    v_dict = topology.adj[u]
    if v in v_dict:
        key, data_dict = min(v_dict[v].items(),
                             key=lambda t:
                             t[1][weight_attr] if weight_attr is not None
                             else 1)
        weight = data_dict[weight_attr] if weight_attr is not None \
            else 1

        if key is None:
            return None, None
        else:
            return (u, v, key), weight
    else:
        return None, None


def find_all_link_keys_with_smallest_weight(topology, u, v, weight_attr):
    """Return ([(u,v,key),...], weight) for all (u,v) links with the smallest `weight_attr` if exists,
    otherwise ([], None)
    """
    if weight_attr is None:
        v_dict = topology.adj[u]
        if v in v_dict:
            return [(u, v, key) for key in v_dict[v]], 1
        else:
            return [], None

    link, weight = find_link_key_with_smallest_weight(topology, u, v, weight_attr)
    if link is None:
        return [], None
    else:
        return [(u, v, key) for key, data_dict in topology.adj[u][v].items() if data_dict[weight_attr] == weight], \
               weight


def find_link_between_nodes_with_smallest_weight(topology, node1, node2, weight_attr, directed=True):
    """Return ((u,v,key), weight) link between the nodes (in both directions) with the smallest `weight_attr` if exists,
    otherwise (None, None)
    """
    link1_2, weight1_2 = find_link_key_with_smallest_weight(topology, node1, node2, weight_attr)
    if directed:
        return link1_2, weight1_2

    link2_1, weight2_1 = find_link_key_with_smallest_weight(topology, node2, node1, weight_attr)
    if weight2_1 is None or (weight1_2 is not None and weight1_2 <= weight2_1):
        return link1_2, weight1_2
    else:
        return link2_1, weight2_1
