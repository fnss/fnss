"""Function to assign and manipulate buffer sizes of network interfaces."""
import networkx as nx
from numpy import mean

from fnss.units import capacity_units, time_units
from fnss.util import extend_link_list_to_all_parallel, \
    find_all_link_keys_with_smallest_weight, reverse_link, find_link_key_with_smallest_weight

__all__ = [
    'set_buffer_sizes_bw_delay_prod',
    'set_buffer_sizes_link_bandwidth',
    'set_buffer_sizes_constant',
    'get_buffer_sizes',
    'clear_buffer_sizes',
]


def set_buffer_sizes_bw_delay_prod(topology, buffer_unit='bytes',
                                   packet_size=1500):
    """
    Assign a buffer sizes proportionally to the product of link bandwidth and
    average network RTT. This is a rule of thumb according to which the buffers
    of Internet routers are generally configured.

    Parameters
    ----------
    topology : (Multi)Topology or (Multi)DirectedTopology
        The topology on which delays are applied.
    buffer_unit : string
        The unit of buffer sizes. Supported units are: *bytes* and *packets*
    packet_size : int, optional
        The average packet size (in bytes). It used only if *packets* is
        selected as buffer size to properly calculate buffer sizes given
        bandwidth and delay values.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.erdos_renyi_topology(50, 0.2)
    >>> fnss.set_capacities_constant(topology, 10, 'Mbps')
    >>> fnss.set_delays_constant(topology, 2, 'ms')
    >>> fnss.set_buffer_sizes_bw_delay_prod(topology)
    """
    try:
        assert all(({'capacity', 'delay'} <= set(data.keys())  # set() for Python 2 compatibility
                    for data in topology.edges.values()))
        capacity_unit = topology.graph['capacity_unit']
        delay_unit = topology.graph['delay_unit']
    except (AssertionError, KeyError):
        raise ValueError('All links must have a capacity and delay attribute')
    topology.graph['buffer_unit'] = buffer_unit
    # this filters potential self-loops which would crash the function
    edges = [edge for edge in topology.edges if edge[0] != edge[1]]
    # dictionary listing all end-to-end routes in which a link appears
    route_presence = dict(zip(edges, [[] for _ in range(len(edges))]))
    # dictionary with all network routes
    route = dict(nx.all_pairs_dijkstra_path(topology, weight='weight'))
    # Dictionary storing end-to-end path delays for each OD pair
    e2e_delay = {}

    for orig, dest_dict in route.items():
        e2e_delay[orig] = {}
        for dest, path in dest_dict.items():
            if len(path) <= 1:
                continue
            path_delay = 0
            for u, v in zip(path[:-1], path[1:]):
                links, delay = find_all_link_keys_with_smallest_weight(topology, u, v, 'delay')

                for link in links:
                    if topology.is_directed() or link in route_presence:
                        route_presence[link].append((orig, dest))
                    # in undirected graphs we might go through edges in opposite direction
                    else:
                        route_presence[reverse_link(link)].append((orig, dest))
                path_delay += delay
            e2e_delay[orig][dest] = path_delay

    # dict containing mean RTT experienced by flows traversing a specific link
    mean_rtt_dict = {}
    for link, route in route_presence.items():
        if route:
            try:
                mean_rtt = mean([e2e_delay[o][d] + e2e_delay[d][o]
                                 for (o, d) in route])
            except KeyError:
                raise ValueError('Cannot assign buffer sizes because some '
                                 'paths do not have corresponding return path')
        else:
            # if this is the case, then this link is not in any shortest path,
            # not even in the one between its endpoint because there is an
            # alternative route with lower cost.
            # In this case we arbitrarily set the RTT as the RTT between the
            # link endpoint if that link was used, i.e. twice the delay of the
            # link
            link_delay = topology.edges[link]['delay']
            if not topology.is_directed():
                mean_rtt = 2 * link_delay
            else:
                reversed_link = reverse_link(link)
                _, reversed_link_delay = find_link_key_with_smallest_weight(topology,
                                                                            reversed_link[0], reversed_link[1], 'delay')
                if reversed_link_delay is not None:
                    mean_rtt = link_delay + reversed_link_delay
                else:
                    try:
                        mean_rtt = link_delay + e2e_delay[reversed_link[0]][reversed_link[1]]
                    except KeyError:
                        raise ValueError('Cannot assign buffer sizes because some '
                                         'paths do not have corresponding return path')
        mean_rtt_dict[link] = mean_rtt
    norm_factor = capacity_units[capacity_unit] * time_units[delay_unit] / 8000.0
    if buffer_unit == 'packets':
        norm_factor /= packet_size
    for link in edges:
        edge = topology.edges[link]
        capacity = edge['capacity']
        edge['buffer'] = int(mean_rtt_dict[link] * capacity * norm_factor)
    return


def set_buffer_sizes_link_bandwidth(topology, k=1.0, default_size=None,
                                    buffer_unit='bytes', packet_size=1500):
    """
    Assign a buffer sizes proportionally to the bandwidth of the interface on
    which the flush. In particularly, the buffer size will be equal to
    :math:`k \times C`, where :math:`C` is the capacity of the link in bps.

    This assignment is equal to the bandwidth-delay product if :math:`k` is the
    average RTT in seconds.

    To use this function, all links of the topology must have a *capacity*
    attribute. If the length of a link cannot be determined, it is applied the
    delay equal *default_delay* if specified, otherwise an error is returned.

    Parameters
    ----------
    topology : (Multi)Topology or (Multi)DirectedTopology
        The topology on which delays are applied.
    k : float, optional
        The multiplicative constant applied to capacity to derive buffer size
    default_size : float, optional
        The buffer size to be applied to interfaces whose speed is unknown. If
        it is None and at least one link does not have a capacity attribute,
        return an error
    buffer_unit : string, unit
        The unit of buffer sizes. Supported units are: *bytes* and *packets*
    packet_size : int, optional
        The average packet size (in bytes). It used only if *packets* is
        selected as buffer size to properly calculate buffer sizes given
        bandwidth and delay values.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.erdos_renyi_topology(50, 0.1)
    >>> fnss.set_capacities_constant(topology, 10, 'Mbps')
    >>> fnss.set_delays_constant(topology, 2, 'ms')
    >>> fnss.set_buffer_sizes_link_bandwidth(topology, k=1.0)
    """
    if k <= 0:
        raise ValueError('k must be a positive number')
    if default_size is None:
        if 'capacity_unit' not in topology.graph \
                or not all(('capacity' in data.keys()
                            for data in topology.edges.values())):
            raise ValueError('All links must have a capacity attribute. '
                             'Set capacity or specify a default buffer size')
    topology.graph['buffer_unit'] = buffer_unit
    # We further dived norm_factor by 8 because buffer unit is bytes
    norm_factor = capacity_units[topology.graph['capacity_unit']] / 8.0
    if buffer_unit == 'packets':
        norm_factor /= packet_size
    for link, data_dict in topology.edges.items():
        if 'capacity' in data_dict:
            capacity = data_dict['capacity']
            buffer_size = int(k * capacity * norm_factor)
        else:
            buffer_size = default_size
        data_dict['buffer'] = buffer_size


def set_buffer_sizes_constant(topology, buffer_size, buffer_unit='bytes', interfaces=None):
    """
    Assign a constant buffer size to all selected interfaces

    Parameters
    ----------
    topology : (Multi)Topology or (Multi)DirectedTopology
        The topology on which buffer sizes are applied.
    buffer_size : int
        The constant buffer_size to be applied to all interface
    buffer_unit : string, unit
        The unit of buffer sizes. Supported units are: *bytes* and *packets*
    interfaces : iterable container of tuples, optional
        Iterable container of selected interfaces on which buffer sizes are
        applied.
        An interface is defined by the tuple (u,v) where u is the node on which
        the interface is located and (u,v) is the link to which the buffer
        flushes. For multigraphs (u,v,key) specifies a link, and (u,v) tuple means every parallel link.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.Topology()
    >>> topology.add_path([1, 2, 4, 5, 8])
    >>> fnss.set_buffer_sizes_constant(topology, 100000, buffer_unit='bytes', \
    ... interfaces=[(1,2), (5,8), (4,5)])
    """
    if buffer_size < 0:
        raise ValueError('The buffer_size argument cannot be negative')
    if interfaces is not None and 'buffer_unit' in topology.graph:
        curr_buffer_unit = topology.graph['buffer_unit']
        if curr_buffer_unit != buffer_unit:
            raise ValueError('The topology already contains buffer sizes ' \
                             'expressed in %s. Use that unit instead of %s' \
                             % (curr_buffer_unit, buffer_unit))
    topology.graph['buffer_unit'] = buffer_unit
    links = topology.edges if interfaces is None else extend_link_list_to_all_parallel(topology, interfaces)
    for link in links:
        topology.edges[link]['buffer'] = buffer_size


def get_buffer_sizes(topology):
    """
    Returns all the buffer sizes.

    Parameters
    ----------
    topology : (Multi)Topology or (Multi)DirectedTopology

    Returns
    -------
    buffer_sizes : dict
        Dictionary of buffer sizes keyed by (u, v) tuple. The key (u, v)
        represents a network interface where u is the node on which the
        interface is located and (u, v) is the link to which the buffer flushes

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.Topology()
    >>> topology.add_path([1, 2, 3])
    >>> fnss.set_buffer_sizes_constant(topology, buffer_size=10)
    >>> buffer = fnss.get_buffer_sizes(topology)
    >>> buffer[(1,2)]
    10
    """
    return nx.get_edge_attributes(topology, 'buffer')


def clear_buffer_sizes(topology):
    """
    Remove all buffer sizes from the topology.

    Parameters
    ----------
    topology : (Multi)Topology or (Multi)DirectedTopology
        The topology whose buffer sizes are cleared
    """
    topology.graph.pop('buffer_unit', None)
    for data_dict in topology.edges.values():
        data_dict.pop('buffer', None)
