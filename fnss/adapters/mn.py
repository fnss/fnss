"""Adapter for Mininet.

This module contains function to convert FNSS topologies into Mininet
topologies and viceversa.
"""
import re

import networkx as nx

from fnss.units import capacity_units, time_units
from fnss.topologies.topology import Topology
from fnss.netconfig import set_delays_constant

__all__ = [
    'from_mininet',
    'to_mininet',
           ]

def from_mininet(topology):
    """Convert a Mininet topology to an FNSS one.

    Parameters
    ----------
    topology : Mininet Topo
        A Mininet topology object

    Returns
    -------
    topology : Topology
        An FNSS Topology object
    """
    fnss_topo = Topology(capacity_unit='Mbps')
    for v in topology.switches():
        fnss_topo.add_node(v, type='switch')
    for v in topology.hosts():
        fnss_topo.add_node(v, type='host')
    for u, v in topology.links():
        fnss_topo.add_edge(u, v)
        opts = topology.linkInfo(u, v)
        if 'bw' in opts:
            fnss_topo.adj[u][v]['capacity'] = opts['bw']
        if 'delay' in opts:
            delay = opts['delay']
            val = re.findall("\d+\.?\d*", delay)[0]
            unit = delay.strip(val).strip(' ')
            set_delays_constant(fnss_topo, val, unit, [(u, v)])
    return fnss_topo


def to_mininet(topology, switches=None, hosts=None, relabel_nodes=True):
    """Convert an FNSS topology to Mininet Topo object that can be used to
    deploy a Mininet network.

    If the links of the topology are labeled with delays, capacities or buffer
    sizes, the returned Mininet topology will also include those parameters.

    However, it should be noticed that buffer sizes are included in the
    converted topology only if they are expressed in packets. If buffer sizes
    are expressed in the form of bytes they will be discarded. This is because
    Mininet only supports buffer sizes expressed in packets.

    Parameters
    ----------
    topology : Topology, DirectedTopology or DatacenterTopology
        An FNSS Topology object
    switches : list, optional
        List of topology nodes acting as switches
    hosts : list, optional
        List of topology nodes acting as hosts
    relabel_nodes : bool, optional
        If *True*, rename node labels according to `Mininet conventions
        <https://github.com/mininet/mininet/wiki/Introduction-to-Mininet#naming-in-mininet>`_.
        In Mininet all node labels are strings whose values are "h1", "h2", ...
        if the node is a host or "s1", "s2", ... if the node is a switch.

    Returns
    -------
    topology : Mininet Topo
        A Mininet topology object

    Notes
    -----
    It is not necessary to provide a list of switch and host nodes if the
    topology object provided are already annotated with a type attribute that
    can have values *host* or *switch*. This is the case of datacenter
    topologies generated with FNSS which already include information about
    which nodes are hosts and which are switches.

    If switches and hosts are passed as arguments, then the hosts and switches
    sets must be disjoint and their union must coincide to the set of all
    topology nodes. In other words, there cannot be nodes labeled as both
    *host* and *switch* and there cannot be nodes that are neither a *host* nor
    a *switch*.

    It is important to point out that if the topology contains loops, it will
    not work with the *ovs-controller* and *controller* provided by Mininet. It
    will be necessary to use custom controllers. Further info `here
    <https://github.com/mininet/mininet/wiki/Introduction-to-Mininet#multipath-routing>`_.
    """
    try:
        from mininet.topo import Topo
    except ImportError:
        raise ImportError('Cannot import mininet.topo package. '
                          'Make sure Mininet is installed on this machine.')
    if hosts is None:
        hosts = (v for v in topology.nodes()
                 if 'host' in topology.node[v]['type'])
    if switches is None:
        switches = (v for v in topology.nodes()
                    if 'switch' in topology.node[v]['type'])
    nodes = set(topology.nodes())
    switches = set(switches)
    hosts = set(hosts)
    if not switches.isdisjoint(hosts):
        raise ValueError('Some nodes are labeled as both host and switch. '
                         'Switches and hosts node lists must be disjoint')
    if nodes != switches.union(hosts):
        raise ValueError('Some nodes are not labeled as either host or switch '
                         'or some nodes listed as switches or hosts do not '
                         'belong to the topology')
    if relabel_nodes:
        hosts = sorted(hosts)
        switches = sorted(switches)
        mapping = dict([(hosts[i], "h%s" % str(i + 1)) for i in range(len(hosts))] +
                       [(switches[i], "s%s" % str(i + 1)) for i in range(len(switches))])
        hosts = set(mapping[v] for v in hosts)
        switches = set(mapping[v] for v in switches)
        nodes = hosts.union(switches)
        topology = nx.relabel_nodes(topology, mapping, copy=True)
    topo = Topo()
    for v in switches:
        topo.addSwitch(str(v))
    for v in hosts:
        topo.addHost(str(v))
    delay_unit = topology.graph.get('delay_unit', None)
    capacity_unit = topology.graph.get('capacity_unit', None)
    buffer_unit = topology.graph.get('buffer_unit', None)
    if capacity_unit:
        capacity_conversion = float(capacity_units[capacity_unit]) \
                              / capacity_units['Mbps']
    if delay_unit:
        delay_conversion = float(time_units[delay_unit]) / time_units['us']
    for u, v in topology.edges():
        params = {}
        if 'capacity' in topology.adj[u][v] and capacity_unit:
            params['bw'] = topology.adj[u][v]['capacity'] * capacity_conversion
            # Use Token Bucket filter to implement rate limit
            params['use_htb'] = True
        if 'delay' in topology.adj[u][v] and delay_unit:
            params['delay'] = '%sus' % str(topology.adj[u][v]['delay']
                                           * delay_conversion)
        if 'buffer_size' in topology.adj[u][v] and buffer_unit == 'packets':
            params['max_queue_size'] = topology.adj[u][v]['buffer_size']
        topo.addLink(str(u), str(v), **params)
    return topo
