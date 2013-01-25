"""
Provides function to assign and manipulate buffer sizes of network interfaces.
"""
import networkx as nx
from numpy import mean
from fnss.util import capacity_units, time_units


__all__ = ['set_buffer_sizes_bw_delay_prod', 
           'set_buffer_sizes_link_bandwidth',
           'set_buffer_sizes_constant',
           'get_buffer_sizes',
           'clear_buffer_sizes',
           ]


def set_buffer_sizes_bw_delay_prod(topology, buffer_unit='bytes', 
                                   packet_size="1500"):
    """
    Assign a buffer sizes proportionally to the product of link bandwidth and 
    average network RTT. This is a rule of thumb according to which the buffers
    of Internet routers are generally configured.

    Parameters
    ----------
    topology : Topology or DirectedTopology
        The topology on which delays are applied.
    buffer_unit : string
        The unit of buffer sizes. Supported units are: "bytes" and "packets"
    mtu : int, optional
        The average packet size of the network. It used only if "packets" is 
        selected as buffer size to properly calculate buffer sizes

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.erdos_renyi_topology(50, 0.2)
    >>> fnss.set_capacities_constant(topology, 10, 'Mbps')
    >>> fnss.set_delays_constant(topology, 2, 'ms')
    >>> fnss.set_buffer_sizes_bw_delay_prod(topology)
    """    
    try:
        assert all(['capacity' in topology.edge[u][v] 
                    for u, v in topology.edges()])
        assert all(['delay' in topology.edge[u][v] 
                    for u, v in topology.edges()])
        capacity_unit = topology.graph['capacity_unit']
        delay_unit = topology.graph['delay_unit']
    except (AssertionError, KeyError):
        raise ValueError('All links must have a capacity and delay attribute')
    topology.graph['buffer_unit'] = buffer_unit
    # this filters potential self-loops which would crash the function
    edges = [(u, v) for (u, v) in topology.edges() if u != v]
    # dictionary listing all end-to-end routes in which a link appears
    route_presence = dict(zip(edges, [[] for _ in range(len(edges))]))
    # dictionary with all network routes
    route = nx.all_pairs_dijkstra_path(topology, weight='weight')
    # Dictionary storing end-to-end path delays for each OD pair
    e2e_delay = {}
    
    for orig in route:
        e2e_delay[orig] = {}
        for dest in route[orig]:
            path = route[orig][dest]
            if len(path) <= 1:
                continue
            path_delay = 0
            for hop in range(len(path) - 1):
                if 'delay' in topology.edge[path[hop]][path[hop + 1]]:
                    if (path[hop], path[hop + 1]) in route_presence:
                        route_presence[(path[hop], path[hop + 1])] \
                                      .append((orig, dest))
                    else:
                        route_presence[(path[hop + 1], path[hop])] \
                                      .append((orig, dest))
                    path_delay += \
                            topology.edge[path[hop]][path[hop + 1]]['delay']
                else:
                    raise ValueError('No link delays available')
            e2e_delay[orig][dest] = path_delay
            
    # dict containing mean RTT experienced by flows traversing a specific link
    mean_rtt_dict = {} 
    for (u, v), route in route_presence.items():
        if len(route) > 0:
            try:
                mean_rtt = mean([e2e_delay[o][d] + e2e_delay[d][o] 
                                 for (o, d) in route])
            except KeyError:
                raise ValueError('Cannot assign buffer sizes because some '
                                 'paths do not have corresponding return path')
        else:
            # if this is the case, then this link is in any shortest path,
            # not even in the one between its endpoint because there is an
            # alternative route with lower cost.
            # In this case we arbitrarily set the RTT as the RTT between the
            # link endpoint if that link was used, i.e. twice the delay of the
            # link
            if (v, u) in edges:
                mean_rtt = topology.edge[u][v]['delay'] + \
                           topology.edge[v][u]['delay']
            else:
                try:
                    mean_rtt = topology.edge[u][v]['delay'] + e2e_delay[v][u]
                except KeyError:
                    raise ValueError('Cannot assign buffer sizes because some '
                                 'paths do not have corresponding return path')
        mean_rtt_dict[(u, v)] = mean_rtt
    norm_factor = capacity_units[capacity_unit] * \
                  time_units[delay_unit] / 8000.0
    if buffer_unit == 'packets':
        norm_factor /= packet_size
    for u, v in edges:
        capacity = topology.edge[u][v]['capacity']
        buffer_size = int(mean_rtt_dict[(u, v)] * capacity * norm_factor)
        topology.edge[u][v]['buffer'] = buffer_size 
    return


def set_buffer_sizes_link_bandwidth(topology, k=1.0, default_size=None, 
                                    buffer_unit='bytes', interfaces=None):
    """
    Assign a buffer sizes proportionally to the bandwidth of the interface on 
    which the flush. In particularly, the buffer size will be equal to k*C,
    where C is the capacity of the link in bps.
    
    To use this function, all links of the topology must have a 'capacity' 
    attribute. If the length of a link cannot be determined, it is applied the 
    delay equal default_delay if specified, otherwise an error is returned. 
    
    Parameters
    ----------
    topology : Topology or DirectedTopology
        The topology on which delays are applied.
    k : float, optional
        The multiplicative constant applied to capacity to derive buffer size
    default_size : float, optional
        The buffer size to be applied to interfaces whose speed is unknown. If
        it is None and at least one link does not have a capacity attribute,
        return an error   
    buffer_unit : string, unit
        The unit of buffer sizes. Supported units are: "bytes" and "packets"
    interfaces : list of tuples, optional
        The list of selected interfaces on which buffer sizes are applied. 
        An interface is defined by the tuple (u,v) where u is the node on which
        the interface is located and (u,v) is the link to which the buffer 
        flushes.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.erdos_renyi_topology(50, 0.1)
    >>> fnss.set_capacities_constant(topology, 10, 'Mbps')
    >>> fnss.set_delays_constant(topology, 2, 'ms')
    >>> fnss.set_buffer_sizes_link_bandwidth(topology, k=1.0)
    """
    edges = topology.edges() if interfaces is None else interfaces
    if default_size is None:
        try:
            [topology.edge[u][v]['capacity'] for u, v in edges]
        except KeyError:
            raise ValueError('All links must have a capacity attribute.'\
                             'Set capacity or specify a default buffer size') 
    topology.graph['buffer_unit'] = buffer_unit
    norm_factor = capacity_units[topology.graph['capacity_unit']]
    for u, v in edges:
        if 'capacity' in topology.edge[u][v]:
            capacity = topology.edge[u][v]['capacity']
            buffer_size = int(k * capacity * norm_factor)
        else: 
            buffer_size = default_size
        topology.edge[u][v]['buffer'] = buffer_size 


def set_buffer_sizes_constant(topology, buffer_size, buffer_unit='bytes', 
                              interfaces=None):
    """
    Assign a constant buffer size to all selected interfaces

    Parameters
    ----------
    topology : Topology or DirectedTopology
        The topology on which buffer sizes are applied.
    buffer_size : int
        The constant buffer_size to be applied to all interface
    buffer_unit : string, unit
        The unit of buffer sizes. Supported units are: "bytes" and "packets"
    interfaces : list of tuples, optional
        The list of selected interfaces on which buffer sizes are applied. 
        An interface is defined by the tuple (u,v) where u is the node on which
        the interface is located and (u,v) is the link to which the buffer 
        flushes.

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
    edges = topology.edges() if interfaces is None else interfaces
    for u, v in edges:
        topology.edge[u][v]['buffer'] = buffer_size



def get_buffer_sizes(topology):
    """
    Returns all the buffer sizes.

    Parameters
    ----------
    topology : Topology or DirectedTopology

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
    topology : Topology or DirectedTopology
        The topology whose buffer sizes are cleared
    """
    if 'buffer_unit' in topology.graph:
        del topology.graph['buffer_unit']
    for u, v in topology.edges():
        if 'buffer' in topology.edge[u][v]:
            del topology.edge[u][v]['buffer']

