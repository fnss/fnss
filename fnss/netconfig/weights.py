"""Functions to assign and manipulate link weights to a network topology."""
import networkx as nx

__all__ = [
    'set_weights_inverse_capacity',
    'set_weights_constant',
    'set_weights_delays',
    'get_weights',
    'clear_weights'
           ]


def set_weights_inverse_capacity(topology):
    """
    Assign link weights to links proportionally to the inverse of their
    capacity. Weights are normalized so that the minimum weight is 1.

    Parameters
    ----------
    topology : Topology
        The topology on which weights are applied.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.Topology()
    >>> topology.add_path([1,2,3,4])
    >>> fnss.set_capacities_constant(topology, 10, 'Mbps')
    >>> fnss.set_weights_inverse_capacity(topology)
    """
    try:
        max_capacity = float(max((topology.adj[u][v]['capacity']
                                  for u, v in topology.edges())))
    except KeyError:
        raise ValueError('All links must have a capacity attribute')
    for u, v in topology.edges():
        capacity = topology.adj[u][v]['capacity']
        weight = max_capacity / capacity
        topology.adj[u][v]['weight'] = weight


def set_weights_delays(topology):
    """
    Assign link weights to links proportionally their delay. Weights are
    normalized so that the minimum weight is 1.

    Parameters
    ----------
    topology : Topology
        The topology on which weights are applied.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.erdos_renyi_topology(50, 0.1)
    >>> fnss.set_delays_constant(topology, 2, 'ms')
    >>> fnss.set_weights_delays(topology)

    """
    try:
        min_delay = float(min((topology.adj[u][v]['delay']
                               for u, v in topology.edges())))
    except KeyError:
        raise ValueError('All links must have a delay attribute')
    for u, v in topology.edges():
        delay = topology.adj[u][v]['delay']
        weight = delay / min_delay
        topology.adj[u][v]['weight'] = weight


def set_weights_constant(topology, weight=1.0, links=None):
    """
    Assign a constant weight to all selected links

    Parameters
    ----------
    topology : Topology
        The topology on which weights are applied.
    weight : float, optional
        The constant weight to be applied to all links
    links : iterable, optional
        Iterable container of selected links on which weights are applied.
        If it is None, all links are selected

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.Topology()
    >>> topology.add_edges_from([(1, 2), (5, 8), (4, 5), (1, 7)])
    >>> fnss.set_weights_constant(topology, weight=1.0, links=[(1, 2), (5, 8), (4, 5)])
    """
    edges = links or topology.edges()
    for u, v in edges:
        topology.adj[u][v]['weight'] = weight


def get_weights(topology):
    """
    Returns all the weights.

    Parameters
    ----------
    topology : Topology

    Returns
    -------
    weights : dict
        Dictionary of weights keyed by link.

    Examples
    --------
    >>> import fnss
    >>> topology = fnss.Topology()
    >>> topology.add_path([1, 2, 3])
    >>> fnss.set_weights_constant(topology, weight=2.0)
    >>> weight = fnss.get_weights(topology)
    >>> weight[(1,2)]
    2.0
    """
    return nx.get_edge_attributes(topology, 'weight')


def clear_weights(topology):
    """
    Remove all weights from the topology.

    Parameters
    ----------
    topology : Topology
    """
    for u, v in topology.edges():
        topology.adj[u][v].pop('weight', None)
