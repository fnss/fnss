"""
Provides functions to assign and manipulate link capacities of a topology.

Link capacities can be assigned either deterministically or randomly, according
to various models.
"""
import networkx as nx
from numpy import cumprod
from fnss.util import random_from_pdf, capacity_units


__all__ = ['set_capacities_constant',
           'set_capacities_random',
           'set_capacities_random_uniform',
           'set_capacities_random_power_law',
           'set_capacities_random_zipf',
           'set_capacities_random_zipf_mandelbrot',
           'set_capacities_degree_gravity',
           'set_capacities_betweenness_gravity',
           'set_capacities_eigenvector_gravity',
           'set_capacities_communicability_gravity',
           'set_capacities_pagerank_gravity',
           'set_capacities_edge_betweenness',
           'set_capacities_edge_communicability',
           'get_capacities',
           'clear_capacities'
           ]

def set_capacities_constant(topology, capacity, capacity_unit='Mbps', 
                            links=None):
    """
    Set constant link capacities
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacity : float
        The value of capacity to set
    links : list, optional
        List of links, represented as (u, v) tuples to which capacity will be 
        set. If None or not specified, the capacity will be applied to all 
        links.
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
        
    Examples
    --------
    >>> import fnss
    >>> topology = fnss.erdos_renyi_topology(50, 0.1)
    >>> fnss.set_capacities_constant(topology, 10, 'Mbps')
    """
    if capacity <= 0:
        raise ValueError('Capacity must be positive')
    if not capacity_unit in capacity_units:
        raise ValueError("The capacity_unit argument is not valid")
    conversion_factor = 1
    if 'capacity_unit' in topology.graph and links is not None:
        # If a capacity_unit is set, that means that some links have already
        # been assigned capacities, so set these capacity using the same unit
        # already used
        curr_capacity_unit = topology.graph['capacity_unit']
        if curr_capacity_unit != capacity_unit:
            conversion_factor = float(capacity_units[capacity_unit]) \
                                / capacity_units[curr_capacity_unit] 
    else:
        topology.graph['capacity_unit'] = capacity_unit
    edges = topology.edges() if links is None else links
    for u, v in edges:
        topology.edge[u][v]['capacity'] = capacity * conversion_factor
    return


def set_capacities_random(topology, capacity_pdf, capacity_unit='Mbps'):
    """
    Set random link capacities according to a given probability density 
    function
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacity_pdf : dict
        A dictionary representing the probability that a capacity value is
        assigned to a link
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    links : list, optional
        List of links, represented as (u, v) tuples to which capacity will be 
        set. If None or not specified, the capacity will be applied to all 
        links.
        
    Examples
    --------
    >>> import fnss
    >>> topology = fnss.erdos_renyi_topology(50, 0.1)
    >>> pdf = {10: 0.5, 100: 0.2, 1000: 0.3}
    >>> fnss.set_capacities_constant(topology, pdf, 'Mbps')
    """
    if not capacity_unit in capacity_units:
        raise ValueError("The capacity_unit argument is not valid")
    if any([capacity < 0 for capacity in capacity_pdf.keys()]):
        raise ValueError('All capacities in capacity_pdf must be positive')
    topology.graph['capacity_unit'] = capacity_unit
    for u, v in topology.edges():
        topology.edge[u][v]['capacity'] = random_from_pdf(capacity_pdf)
    return


def set_capacities_random_power_law(topology, capacities, capacity_unit='Mbps', 
                                    reverse=False):
    """
    Set random link capacities according to a power-law probability density 
    function.
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    reverse : bool, optional
        If False, lower capacity links are the most frequent, if True, higher
        capacity links are more frequent
    """
    capacities = sorted(capacities, reverse=reverse)
    rel_capacities = [float(capacities[i+1])/float(capacities[i]) 
                      for i in range(len(capacities) - 1)]
    rel_capacities.insert(0, 1.0)
    rel_capacities = cumprod(rel_capacities)
    pdf = [1.0/rel_capacities[i] for i in range(len(rel_capacities))]
    norm_factor = sum(pdf)
    norm_pdf = {capacities[i]: pdf[i]/norm_factor 
                for i in range(len(capacities))}
    set_capacities_random(topology, norm_pdf, capacity_unit=capacity_unit)


def set_capacities_random_zipf_mandelbrot(topology, capacities, 
                                          capacity_unit='Mbps', alpha=1.1, 
                                          q=0.0, reverse=False):
    """
    Set random link capacities according to a Zipf-Mandelbrot probability 
    density function.
    
    This capacity allocation consists in the following steps:
    
    1. All capacities are sorted in descending or order (or ascending if
       reverse is True)
    
    2. The i-th value of the sorted capacities list is then assigned to a link
       with probability
       
    .. math::
       p(i) = \\frac{1/(i + q)^\\alpha}{\\sum_{i = 1}^{N}{1/(i + q)^\\alpha}}.
    
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    alpha : float, default 1.1
        The :math`\alpha` parameter of the Zipf-Mandlebrot density function
    q : float, default 0
        The :math`q` parameter of the Zipf-Mandlebrot density function
    reverse : bool, optional
        If False, lower capacity links are the most frequent, if True, higher
        capacity links are more frequent
    """
    if alpha <= 0.0:
        raise ValueError('alpha must be positive')
    capacities = sorted(capacities, reverse=reverse)
    pdf = {capacities[i]: 1.0 /(i + 1.0 + q)**alpha 
           for i in range(len(capacities))}
    norm_factor = sum(pdf.values())
    norm_pdf = {capacity: pdf[capacity]/norm_factor for capacity in pdf}
    set_capacities_random(topology, norm_pdf, capacity_unit=capacity_unit)


def set_capacities_random_zipf(topology, capacities, capacity_unit='Mbps', 
                               alpha=1.1,  reverse=False):
    """
    Set random link capacities according to a Zipf probability density 
    function.
    
    The same objective can be achieved by invoking the function
    ''set_capacities_random_zipf_mandlebrot'' with parameter q set to 0.
    
    This capacity allocation consists in the following steps:
    
    1. All capacities are sorted in descending or order (or ascending if
       reverse is True)
    
    2. The i-th value of the sorted capacities list is then assigned to a link
       with probability
       
    .. math::
            p(i) = \\frac{1/i^\\alpha}{\\sum_{i = 1}^{N}{1/i^\\alpha}}.
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    alpha : float, default 1.1
        The :math`\alpha` parameter of the Zipf density function
    reverse : bool, optional
        If False, lower capacity links are the most frequent, if True, higher
        capacity links are more frequent
    """
    set_capacities_random_zipf_mandelbrot(topology, capacities, alpha=alpha, 
                                          q=0.0, reverse=reverse, 
                                          capacity_unit=capacity_unit)


def set_capacities_random_uniform(topology, capacities, capacity_unit='Mbps'):
    """
    Set random link capacities according to a uniform probability density
    function.
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    """
    capacity_pdf = {capacity: 1.0/len(capacities) for capacity in capacities}
    set_capacities_random(topology, capacity_pdf, capacity_unit=capacity_unit)


def set_capacities_degree_gravity(topology, capacities, capacity_unit='Mbps'):
    """
    Set link capacities proportionally to the product of the degrees of the 
    two end-points of the link

    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    """
    if topology.is_directed():
        in_degree = nx.in_degree_centrality(topology)
        out_degree = nx.out_degree_centrality(topology)
        gravity = {(u, v): out_degree[u] * in_degree[v] 
                   for (u, v) in topology.edges()}
    else:
        degree = nx.degree_centrality(topology)
        gravity = {(u, v): degree[u] * degree[v] 
                   for (u, v) in topology.edges()}
    _set_capacities_proportionally(topology, capacities, gravity, 
                                   capacity_unit=capacity_unit)


def set_capacities_betweenness_gravity(topology, capacities, 
                                       capacity_unit='Mbps', weighted=True):
    """
    Set link capacities proportionally to the product of the betweenness
    centralities of the two end-points of the link
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    weighted : bool, optional
        Indicate whether link weights need to be used to compute shortest
        paths. If links do not have link weights or this parameter is False,
        shortest paths are calculated based on hop count.
    """
    weight = 'weight' if weighted else None
    centrality = nx.betweenness_centrality(topology, normalized=False, 
                                           weight=weight)
    _set_capacities_gravity(topology, capacities, centrality, capacity_unit)


def set_capacities_eigenvector_gravity(topology, capacities, 
                                       capacity_unit='Mbps', max_iter=1000):
    """
    Set link capacities proportionally to the product of the eigenvector
    centralities of the two end-points of the link
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    max_iter : int, optional
        The max number of iteration of the algorithm allowed. If a solution is
        not found within this period
    
    Raises
    ------
    RuntimeError : if the algorithm does not converge in max_iter iterations
    """
    try:
        centrality = nx.eigenvector_centrality(topology, max_iter=max_iter)
    except nx.NetworkXError:
        raise RuntimeError('Algorithm did not converge in %d iterations' 
                           % max_iter)
    _set_capacities_gravity(topology, capacities, centrality, capacity_unit)


def set_capacities_pagerank_gravity(topology, capacities, capacity_unit='Mbps', 
                                    alpha=0.85, weight=None):
    """
    Set link capacities proportionally to the product of the Pagerank
    centralities of the two end-points of the link
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    alpha : float, optional
        The apha parameter of the PageRank algorithm
    weight : str, optional
        The name of the link attribute to use for the PageRank algorithm. Valid
        attributes include *capacity* *delay* and *weight*. If ``None``, all
        links are assigned the same weight.
    """
    centrality = nx.pagerank_numpy(topology, alpha=alpha, personalization=None, 
                             weight=weight)
    _set_capacities_gravity(topology, capacities, centrality, capacity_unit)


def set_capacities_communicability_gravity(topology, capacities, 
                                           capacity_unit='Mbps'):
    """
    Set link capacities proportionally to the product of the communicability
    centralities of the two end-points of the link
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    """
    centrality = nx.communicability_centrality(topology)
    _set_capacities_gravity(topology, capacities, centrality, capacity_unit)


def set_capacities_edge_betweenness(topology, capacities, capacity_unit='Mbps', 
                                    weighted=True):
    """
    Set link capacities proportionally to edge betweenness centrality of the
    link.
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    weighted : bool, optional
        Indicate whether link weights need to be used to compute shortest
        paths. If links do not have link weights or this parameter is False,
        shortest paths are calculated based on hop count.
    """
    weight = 'weight' if weighted else None
    centrality = nx.edge_betweenness_centrality(topology, normalized=False, 
                                                weight=weight)
    _set_capacities_proportionally(topology, capacities, centrality, 
                                   capacity_unit=capacity_unit)


def set_capacities_edge_communicability(topology, capacities, 
                                        capacity_unit='Mbps'):
    """
    Set link capacities proportionally to edge communicability centrality of
    the link.
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    """
    communicability = nx.communicability(topology)
    centrality = {(u, v): communicability[u][v] for (u, v) in topology.edges()}
    _set_capacities_proportionally(topology, capacities, centrality, 
                                   capacity_unit=capacity_unit)


def _set_capacities_gravity(topology, capacities, node_metric, 
                            capacity_unit='Mbps'):
    """
    Set link capacities proportionally to the product of the values of a given
    node metric of the two end-points of the link

    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    node_metric : dict
        A dictionary with all values of the given node metric, keyed by node
        name
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    """
    gravity = {(u, v): node_metric[u] * node_metric[v] 
               for (u, v) in topology.edges()}
    _set_capacities_proportionally(topology, capacities, gravity, 
                                   capacity_unit=capacity_unit)


def _set_capacities_proportionally(topology, capacities, metric, 
                                   capacity_unit='Mbps'):
    """
    Set link capacities proportionally to the product of the values of a given
    edge metric of the link
    
    Parameters
    ----------
    topology : Topology
        The topology to which link capacities will be set
    capacities : list
        A list of all possible capacity values
    node_metric : dict
        A dictionary with all values of the given node metric, keyed by node
        name
    capacity_unit : str, optional
        The unit in which capacity value is expressed (e.g. Mbps, Gbps etc..)
    """
    if not capacity_unit in capacity_units:
        raise ValueError("The capacity_unit argument is not valid")
    if any([capacity < 0 for capacity in capacities]):
        raise ValueError('All capacities must be positive')
    topology.graph['capacity_unit'] = capacity_unit
    
    # get min and max of selected edge metric
    min_metric = min(metric.values())
    max_metric = max(metric.values())
    
    capacities = sorted(capacities)
    
    min_capacity = capacities[0] - 0.5 * (capacities[1] - capacities[0])
    max_capacity = capacities[-1] + 0.5 * (capacities[-1] - capacities[-2])
    capacity_boundaries = [0.5*(capacities[i] + capacities[i + 1]) 
                           for i in range(len(capacities) - 1)]
    capacity_boundaries.append(max_capacity)
    
    metric_boundaries = [(capacity_boundary - min_capacity) * 
                         ((max_metric - min_metric)/
                          (max_capacity - min_capacity)) + min_metric 
                         for capacity_boundary in capacity_boundaries]
    # to prevent float rounding errors
    metric_boundaries[len(metric_boundaries) - 1] += 0.001
    
    for (u, v), metric_value in metric.items():
        for i in range(len(metric_boundaries)):
            if metric_value <= metric_boundaries[i]:
                capacity = capacities[i]
                topology.edge[u][v]['capacity'] = capacity
                break
   

def get_capacities(topology):
    """
    Returns a dictionary with all link capacities.

    Parameters
    ----------
    topology : Topology
        The topology whose link delays are requested

    Returns
    -------
    capacities : dict
        Dictionary of link capacities keyed by link.
    
    Examples
    --------
    >>> import fnss
    >>> topology = fnss.Topology()
    >>> topology.add_path([1,2,3])
    >>> fnss.set_capacities_constant(topology, 10, 'Mbps')
    >>> capacity = get_capacities(topology)
    >>> capacity[(1,2)]
    10
    """
    return nx.get_edge_attributes(topology, 'capacity')


def clear_capacities(topology):
    """
    Remove all capacities from the topology.

    Parameters
    ----------
    topology : Topology
    """
    if 'capacity_unit' in topology.graph:
        del topology.graph['capacity_unit']
    for u, v in topology.edges():
        if 'capacity' in topology.edge[u][v]:
            del topology.edge[u][v]['capacity']

