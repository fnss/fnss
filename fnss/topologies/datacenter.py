"""Functions to generate commonly adopted datacenter topologies.

Each topology generation function returns an instance of DatacenterTopology
"""
import networkx as nx
from fnss.topologies.topology import Topology


__all__ = [
    'DatacenterTopology',
    'two_tier_topology',
    'three_tier_topology',
    'bcube_topology',
    'fat_tree_topology'
           ]


class DatacenterTopology(Topology):
    """
    Represent a datacenter topology
    """

    def number_of_switches(self):
        """
        Return the number of switches in the topology
        """
        return len(self.switches())

    def number_of_hosts(self):
        """
        Return the number of hosts in the topology
        """
        return len(self.hosts())

    def switches(self):
        """
        Return the list of switch nodes in the topology
        """
        return [v for v in self.nodes() if self.node[v]['type'] == 'switch']

    def hosts(self):
        """
        Return the list of host nodes in the topology
        """
        return [v for v in self.nodes() if self.node[v]['type'] == 'host']


def two_tier_topology(n_core, n_edge, n_hosts):
    """
    Return a two-tier datacenter topology.

    This topology comprises switches organized in two tiers (core and edge) and
    hosts connected to edge routers. Each core switch is connected to each
    edge switch while each host is connected to exactly one edge switch.

    Each node has two attributes:
     * type: can either be *switch* or *host*
     * tier: can either be *core*, *edge* or *leaf*. Nodes in the leaf tier are
       only host, while all core and edge nodes are switches.

    Each edge has an attribute type as well which can either be *core_edge* if
    it connects a core and an edge switch or *edge_leaf* if it connects an edge
    switch to a host.

    Parameters
    ----------
    n_core : int
        Total number of core switches
    n_edge : int
        Total number of edge switches
    n_hosts : int
        Number of hosts connected to each edge switch.

    Returns
    -------
    topology : DatacenterTopology
    """
    # validate input arguments
    if not all(isinstance(n, int) for n in (n_core, n_edge, n_hosts)):
        raise TypeError('n_core, n_edge and n_hosts must be integers')
    if n_core < 1 or n_edge < 1 or n_hosts < 1:
        raise ValueError('n_core, n_edge and n_hosts must be positive')

    topo = DatacenterTopology(nx.complete_bipartite_graph(n_core, n_edge))
    topo.name = "two_tier_topology(%d,%d,%d)" % (n_core, n_edge, n_hosts)
    topo.graph['type'] = 'two_tier'
    for u in range(n_core):
        topo.node[u]['tier'] = 'core'
        topo.node[u]['type'] = 'switch'
        for v in topo.adj[u]:
            topo.adj[u][v]['type'] = 'core_edge'
    for u in range(n_core, n_core + n_edge):
        topo.node[u]['tier'] = 'edge'
        topo.node[u]['type'] = 'switch'
        for _ in range(n_hosts):
            v = topo.number_of_nodes()
            topo.add_node(v)
            topo.node[v]['tier'] = 'leaf'
            topo.node[v]['type'] = 'host'
            topo.add_edge(u, v, type='edge_leaf')
    return topo


def three_tier_topology(n_core, n_aggregation, n_edge, n_hosts):
    """
    Return a three-tier data center topology.

    This topology  comprises switches organized in three tiers (core,
    aggregation and edge) and hosts connected to edge routers. Each core
    switch is connected to each aggregation, each edge switch is connected to
    one aggregation switch and finally each host is connected to exactly one
    edge switch.

    Each node has two attributes:
     * type: can either be *switch* or *host*
     * tier: can either be *core*, *aggregation*, *edge* or *leaf*. Nodes in
       the leaf tier are only host, while all core, aggregation and edge
       nodes are switches.

    Each edge has an attribute type as well which can either be *core_edge* if
    it connects a core and an aggregation switch, *aggregation_edge*, if it
    connects an aggregation and a core switch or *edge_leaf* if it connects an
    edge switch to a host.

    The total number of hosts is
    :math:`n_{aggregation} * n_{edge} * n_{hosts}`.

    Parameters
    ----------
    n_core : int
        Total number of core switches
    n_aggregation : int
        Total number of aggregation switches
    n_edge : int
        Number of edge switches per each each aggregation switch
    n_hosts : int
        Number of hosts connected to each edge switch.

    Returns
    -------
    topology : DatacenterTopology
    """
    # Validate input arguments
    if not all(isinstance(n, int) for n in
               (n_core, n_aggregation, n_edge, n_hosts)):
        raise TypeError('n_core, n_edge, n_aggregation and n_hosts '\
                        'must be integers')
    if n_core < 1 or n_aggregation < 1 or n_edge < 1 or n_hosts < 1:
        raise ValueError('n_core, n_aggregation, n_edge and n_host '\
                         'must be positive')

    topo = DatacenterTopology(nx.complete_bipartite_graph(n_core,
                                                          n_aggregation))
    topo.name = "three_tier_topology(%d,%d,%d,%d)" % (n_core, n_aggregation,
                                                      n_edge, n_hosts)
    topo.graph['type'] = 'three_tier'
    for u in range(n_core):
        topo.node[u]['tier'] = 'core'
        topo.node[u]['type'] = 'switch'
        for v in topo.adj[u]:
            topo.adj[u][v]['type'] = 'core_aggregation'
    for u in range(n_core, n_core + n_aggregation):
        topo.node[u]['tier'] = 'aggregation'
        topo.node[u]['type'] = 'switch'
        for _ in range(n_edge):
            v = topo.number_of_nodes()
            topo.add_node(v)
            topo.node[v]['tier'] = 'edge'
            topo.node[v]['type'] = 'switch'
            topo.add_edge(u, v, type='aggregation_edge')
    total_n_edge = topo.number_of_nodes()
    for u in range(n_core + n_aggregation, total_n_edge):
        for _ in range(n_hosts):
            v = topo.number_of_nodes()
            topo.add_node(v)
            topo.node[v]['tier'] = 'leaf'
            topo.node[v]['type'] = 'host'
            topo.add_edge(u, v, type='edge_leaf')
    return topo


def bcube_topology(n, k):
    """
    Return a Bcube datacenter topology, as described in [1]_:

    The BCube topology is a topology specifically designed for
    shipping-container based, modular data centers. A BCube topology comprises
    hosts with multiple network interfaces connected to commodity switches. It
    has the peculiar characteristic that switches are never directly connected
    to each other and hosts are used also for packet forwarding. This
    topology is defined as a recursive structure. A :math:`Bcube_0` is composed
    of n hosts connected to an n-port switch. A :math:`Bcube_1` is composed
    of n :math:`Bcube_0` connected to n n-port switches. A :math:`Bcube_k` is
    composed of n :math:`Bcube_{k-1}` connected to :math:`n^k` n-port switches.

    This topology comprises:
     * :math:`n^(k+1)` hosts, each of them connected to :math:`k+1` switches
     * :math:`n*(k+1)` switches, each of them having n ports

    Each node has an attribute type which can either be *switch* or *host*
    and an attribute *level* which specifies at what level of the Bcube
    hierarchy it is located.

    Each edge also has the attribute *level*.

    Parameters
    ----------
    k : int
        The level of Bcube
    n : int
        The number of host per :math:`Bcube_0`

    Returns
    -------
    topology : DatacenterTopology

    References
    ----------
    .. [1] C. Guo, G. Lu, D. Li, H. Wu, X. Zhang, Y. Shi, C. Tian, Y. Zhang,
       and S. Lu.  BCube: a high performance, host-centric network
       architecture for modular data centers. Proceedings of the ACM SIGCOMM
       2009 conference on Data communication (SIGCOMM '09). ACM, New York, NY,
       USA. http://doi.acm.org/10.1145/1592568.1592577
    """
    # Validate input arguments
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError('k and n arguments must be of int type')
    if n < 1:
        raise ValueError("Invalid n parameter. It should be >= 1")
    if k < 0:
        raise ValueError("Invalid k parameter. It should be >= 0")

    topo = DatacenterTopology(type='bcube')
    topo.name = "bcube_topology(%d,%d)" % (n, k)

    # add hosts
    n_hosts = n ** (k + 1)
    topo.add_nodes_from(range(n_hosts), type='host')

    # add all layers of switches and connect them to hosts
    for level in range(k + 1):
        # i is the horizontal position of a switch a specific level
        for i in range(n ** k):
            u = topo.number_of_nodes()
            # add switch at given level
            topo.add_node(u, level=level, type='switch')
            hosts = range(i, i + n ** (level + 1), n ** level)
            for v in hosts:
                topo.add_edge(u, v, level=level)
    return topo


def fat_tree_topology(k):
    """
    Return a fat tree datacenter topology, as described in [1]_

    A fat tree topology built using k-port switches can support up to
    :math:`(k^3)/4` hosts. This topology comprises k pods with two layers of
    :math:`k/2` switches each. In each pod, each aggregation switch is
    connected to all the :math:`k/2` edge switches and each edge switch is
    connected to :math:`k/2` hosts. There are :math:`(k/2)^2` core switches,
    each of them connected to one aggregation switch per pod.

    Each node has three attributes:
     * type: can either be *switch* or *host*
     * tier: can either be *core*, *aggregation*, *edge* or *leaf*. Nodes in
     * pod: the pod id in which the node is located, unless it is a core switch
       the leaf tier are only host, while all core, aggregation and edge
       nodes are switches.

    Each edge has an attribute type as well which can either be *core_edge* if
    it connects a core and an aggregation switch, *aggregation_edge*, if it
    connects an aggregation and a core switch or *edge_leaf* if it connects an
    edge switch to a host.

    Parameters
    ----------
    k : int
        The number of ports of the switches

    Returns
    -------
    topology : DatacenterTopology

    References
    ----------
    .. [1] M. Al-Fares, A. Loukissas, and A. Vahdat. A scalable, commodity
       data center network architecture. Proceedings of the ACM SIGCOMM 2008
       conference on Data communication (SIGCOMM '08). ACM, New York, NY, USA
       http://doi.acm.org/10.1145/1402958.1402967
    """
    # validate input arguments
    if not isinstance(k, int):
        raise TypeError('k argument must be of int type')
    if k < 1 or k % 2 == 1:
        raise ValueError('k must be a positive even integer')

    topo = DatacenterTopology(type='fat_tree')
    topo.name = "fat_tree_topology(%d)" % (k)

    # Create core nodes
    n_core = (k // 2) ** 2
    topo.add_nodes_from([v for v in range(int(n_core))],
                        layer='core', type='switch')

    # Create aggregation and edge nodes and connect them
    for pod in range(k):
        aggr_start_node = topo.number_of_nodes()
        aggr_end_node = aggr_start_node + k // 2
        edge_start_node = aggr_end_node
        edge_end_node = edge_start_node + k // 2
        aggr_nodes = range(aggr_start_node, aggr_end_node)
        edge_nodes = range(edge_start_node, edge_end_node)
        topo.add_nodes_from(aggr_nodes, layer='aggregation',
                            type='switch', pod=pod)
        topo.add_nodes_from(edge_nodes, layer='edge', type='switch', pod=pod)
        topo.add_edges_from([(u, v) for u in aggr_nodes for v in edge_nodes],
                            type='aggregation_edge')
    # Connect core switches to aggregation switches
    for core_node in range(n_core):
        for pod in range(k):
            aggr_node = n_core + (core_node // (k // 2)) + (k * pod)
            topo.add_edge(core_node, aggr_node, type='core_aggregation')
    # Create hosts and connect them to edge switches
    for u in [v for v in topo.nodes() if topo.node[v]['layer'] == 'edge']:
        leaf_nodes = range(topo.number_of_nodes(),
                           topo.number_of_nodes() + k // 2)
        topo.add_nodes_from(leaf_nodes, layer='leaf', type='host',
                            pod=topo.node[u]['pod'])
        topo.add_edges_from([(u, v) for v in leaf_nodes], type='edge_leaf')
    return topo
