"""Adapter for AutoNetkit.

This module contains function for converting FNSS Topology objects into
NetworkX graph objects compatible with AutoNetKit and viceversa.
"""
from fnss import rename_edge_attribute


__all__ = [
    'from_autonetkit',
    'to_autonetkit'
           ]


def to_autonetkit(topology):
    """Convert an FNSS topology into a NetworkX graph object compatible for
    AutoNetKit.

    The returned graph can be saved into a GraphML file using NetworkX
    *write_graphml* function and then passed to AutoNetKit as command line
    parameter.

    The current implementation of this function only renames the weight
    attribute from *weight* to *ospf_cost*

    Parameters
    ----------
    topology : FNSS Topology
        Autonetkit topology object

    Returns
    -------
    ank_graph : FNSS topology
        an FNSS topology compatible for import to AutoNetKit
    """
    topology = topology.copy()
    rename_edge_attribute(topology, 'weight', 'ospf_cost')
    return topology


def from_autonetkit(topology):
    """Convert an AutoNetKit graph into an FNSS Topology object.

    The current implementation of this function only renames the weight
    attribute from *weight* to *ospf_cost*

    Parameters
    ----------
    topology : NetworkX graph
        An AutoNetKit NetworkX graph

    Returns
    -------
    fnss_topology : FNSS Topology
        FNSS topology
    """
    topology = topology.copy()
    rename_edge_attribute(topology, 'ospf_cost', 'weight')
    return topology
