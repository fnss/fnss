"""Functions to assign and manipulate link delays."""
import networkx as nx
from fnss.units import time_units, distance_units

__all__ = [
    'PROPAGATION_DELAY_VACUUM',
    'PROPAGATION_DELAY_FIBER',
    'set_delays_constant',
    'set_delays_geo_distance',
    'get_delays',
    'clear_delays'
           ]

# Propagation delay of light in the vacuum
PROPAGATION_DELAY_VACUUM = 1.0 / 300  # ms/Km

# Propagation delay of light in an average optical fiber
PROPAGATION_DELAY_FIBER = 0.005  # ms/Km


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
        List of selected links on which weights are applied. If it is None,
        all links are selected

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
    edges = links or topology.edges()
    for u, v in edges:
        topology.adj[u][v]['delay'] = delay * conversion_factor


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
    specific_delay : float
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
    >>> fnss.set_delays_geo_distance(topology, specific_delay=fnss.PROPAGATION_DELAY_FIBER)
    """
    # Validate input parameters
    if not delay_unit in time_units:
        raise ValueError("The delay_unit argument is not valid")
    if not 'distance_unit' in topology.graph:
        raise ValueError("The provided topology does not have a "\
                         "distance_unit attribute")
    distance_unit = topology.graph['distance_unit']
    if distance_unit not in distance_units:
        raise ValueError("The distance_unit attribute of the provided "\
                         "topology (%s) is not valid" % distance_unit)
    edges = links or topology.edges()
    if default_delay is None:
        if any(('length' not in topology.adj[u][v] for u, v in edges)):
            raise ValueError('All links must have a length attribute')
    if 'delay_unit' in topology.graph and links is not None:
        # If a delay_unit is set, that means that some links have already
        # been assigned delays, so set these delays using the same unit
        # already used instead of the delay unit provided as argument
        curr_delay_unit = topology.graph['delay_unit']
        conv_factor = 1.0 / time_units[curr_delay_unit]
    else:
        topology.graph['delay_unit'] = delay_unit
        curr_delay_unit = delay_unit  # used in case of default delay assignment
        conv_factor = 1.0 / time_units[delay_unit]
    # factor to convert length value in Km
    length_conv_factor = distance_units[distance_unit]
    # factor to convert default delay in target delay unit
    default_conv_factor = time_units[delay_unit] / time_units[curr_delay_unit]
    for u, v in edges:
        if 'length' in topology.adj[u][v]:
            length = topology.adj[u][v]['length'] * length_conv_factor
            delay = specific_delay * length * conv_factor
        else:
            delay = default_delay * default_conv_factor
        topology.adj[u][v]['delay'] = delay


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
    topology.graph.pop('delay_unit', None)
    for u, v in topology.edges():
        topology.adj[u][v].pop('delay', None)
