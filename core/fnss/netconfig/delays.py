"""
Provides functions to assign and manipulate link delays.
"""
from math import sqrt
import networkx as nx
from fnss.util import time_units

__all__ = ['PROPAGATION_DELAY_VACUUM',
           'PROPAGATION_DELAY_FIBER',
           'set_delays_constant', 
           'set_delays_geo_distance', 
           'get_delays', 
           'clear_delays']

# Propagation delay of light in the vacuum
PROPAGATION_DELAY_VACUUM = 1.0/300 # ms/Km

# Propagation delay of light in an average optical fiber
PROPAGATION_DELAY_FIBER = 0.005 # ms/Km


def set_delays_constant(topology, delay=1.0, delay_unit='ms', links=None):
    """
    Assign a constant delay to all selected links

    Parameters
    ----------
    topology : Topology
        The topology on which delays are applied.
    delay : float, optional
        The constant delay to be applied to all links
    delay_unit : string, optional
        The unit of delays. Supported units are: "us" (microseconds), "ms" 
        (milliseconds) and "s" (seconds)
    links : list, optional
        List of selected links on which weights are applied. If it is None, all
        links are selected

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.Topology()
    >>> topology.add_path([1, 2, 4, 5, 8])
    >>> fnss.set_delays_constant(topology, 5.0, 'ms', links=[(1,2), (5,8), (4,5)])
    >>> delay = fnss.get_delays(topology)
    >>> delay[(1, 2)]
    5.0
    """
    if not delay_unit in time_units:
        raise ValueError("The delay_unit argument is not valid")
    conversion_factor = 1
    if 'delay_unit' in topology.graph and links is not None:
        # If a delay_unit is set, that means that some links have already
        # been assigned delays, so set these delay using the same unit
        # already used
        curr_delay_unit = topology.graph['delay_unit']
        if curr_delay_unit != delay_unit:
            conversion_factor = float(time_units[delay_unit]) \
                                / time_units[curr_delay_unit] 
    else:
        topology.graph['delay_unit'] = delay_unit
    edges = topology.edges() if links is None else links
    for u, v in edges:
        topology.edge[u][v]['delay'] = delay * conversion_factor


def set_delays_geo_distance(topology, specific_delay, default_delay=None, 
                            delay_unit='ms', links=None):
    """
    Assign a delay to all selected links equal to the product of link length
    and specific delay. To use this function, all nodes must have a 'latitude'
    and a 'longitude' attribute. Alternatively, all links of the topology must 
    have a 'length' attribute. If the length of a link cannot be determined, it
    is applied the delay equal default_delay if specified, otherwise an error 
    is returned. 
    
    Parameters
    ----------
    topology : Topology
        The topology on which delays are applied.
    specific_delay : float, optional
        The specific delay (in ms/Km) to be applied to all links
    default_delay : float, optional
        The delay to be applied to links whose length is not known. If None, if
        the length of a link cannot be determined, an error is returned    
    delay_unit : string, optional
        The unit of delays. Supported units are: "us" (microseconds), "ms" 
        (milliseconds) and "s" (seconds)
    links : list, optional
        List of selected links on which weights are applied. If it is None, all
        links are selected

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.parse_abilene('abilene_topo.txt')
    >>> fnss.set_delays_geo_distance(topology, specific_delay=fnss.PROP_DELAY_FIBER)
    """
    if not delay_unit in time_units:
        raise ValueError("The delay_unit argument is not valid") 
    edges = topology.edges() if links is None else links
    if default_delay is None:
        if not all(['length' in topology.edge[u][v] for u, v in edges]):
            if not all(['latitude' in topology.node[v] and \
                        'longitude' in topology.node[v] and \
                        'latitude' in topology.node[u] and \
                        'longitude' in topology.node[u] 
                        for u, v in edges]):
                raise ValueError('All links must have a length attribute or '\
                   'at all nodes must have a latitude and longitude attribute')
        conversion_factor = 1
    if 'delay_unit' in topology.graph and links is not None:
        # If a delay_unit is set, that means that some links have already
        # been assigned delays, so set these delay using the same unit
        # already used
        curr_delay_unit = topology.graph['delay_unit']
        if curr_delay_unit != delay_unit:
            conversion_factor = float(time_units[delay_unit]) \
                                / time_units[curr_delay_unit] 
    else:
        topology.graph['delay_unit'] = delay_unit
    for u, v in edges:
        if 'length' in topology.edge[u][v]:
            length = topology.edge[u][v]['length']
            delay = specific_delay * length
        elif 'longitude' in topology.node[u] and \
             'latitude' in topology.node[u] and \
             'longitude' in topology.node[v] and \
             'latitude' in topology.node[v]:
            x_v = float(topology.node[v]['longitude'])
            y_v = float(topology.node[v]['latitude'])
            x_u = float(topology.node[u]['longitude'])
            y_u = float(topology.node[u]['latitude'])  
            length = sqrt((x_v - x_u)**2 + (y_v - y_u)**2)
            delay = specific_delay * length
        else:
            delay = default_delay
        topology.edge[u][v]['delay'] = delay * conversion_factor


def get_delays(topology):
    """
    Returns all the delays.

    Parameters
    ----------
    topology : Topology
        The topology whose link delays are requested

    Returns
    -------
    delays : dict
        Dictionary of link delays keyed by link.
    
    Examples
    --------
    >>> import fnss
    >>> topology = fnss.Topology()
    >>> topology.add_path([1,2,3])
    >>> fnss.set_delays_constant(topology, 10, 'ms')
    >>> delay = get_delays(topology)
    >>> delay[(1,2)]
    10
    """
    return nx.get_edge_attributes(topology, 'delay')


def clear_delays(topology):
    """
    Remove all delays from the topology.

    Parameters
    ----------
    topology : Topology
        
    """
    if 'delay_unit' in topology.graph:
        del topology.graph['delay_unit']
    for u, v in topology.edges():
        if 'delay' in topology.edge[u][v]:
            del topology.edge[u][v]['delay']
