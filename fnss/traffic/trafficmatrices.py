"""Functions and classes for creating and manipulating traffic matrices.

The functions of this class allow users to synthetically generate traffic
matrices with given statistical properties according to models proposed in
literature.

The output of this generation is either a TrafficMatrix or a
TrafficMatrixSequence object.

A traffic matrix or a sequence of matrices can be read and written from/to an
XML files with provided functions.
"""
import itertools
import multiprocessing as mp
from math import exp, sin, pi, log, sqrt
from collections import Counter
import xml.etree.cElementTree as ET

from numpy import isinf
from numpy.random import lognormal, normal
import networkx as nx

from fnss.units import capacity_units, time_units
import fnss.util as util
from fnss.topologies.topology import fan_in_out_capacities, \
                                     od_pairs_from_topology


__all__ = [
    'TrafficMatrix',
    'TrafficMatrixSequence',
    'static_traffic_matrix',
    'stationary_traffic_matrix',
    'sin_cyclostationary_traffic_matrix',
    'read_traffic_matrix',
    'write_traffic_matrix',
    'validate_traffic_matrix',
    'link_loads'
           ]


class TrafficMatrix(object):
    """
    Class representing a single traffic matrix.

    It simply contains a set of traffic volumes being exchanged between
    origin-destination pairs

    Parameters
    ----------
    volume_unit : str
        The unit in which traffic volumes are expressed
    flows : dict, optional
        The traffic volumes or the matrix, keyed by origin-destination pair.
        The origin-destination pair is a tuple whose two elements are
        respectively the identifier of the origin and destination nodes and
        volumes are all expressed in the same unit
    """

    def __init__(self, volume_unit='Mbps', flows=None):
        """
        Initialize the traffic matrix
        """
        if not volume_unit in capacity_units:
            raise ValueError("The volume_unit argument is not valid")
        self.attrib = {}
        self.attrib['volume_unit'] = volume_unit
        self.flow = flows if flows is not None else {}
        return

    def __iter__(self):
        """
        Iterates over the flows.

        Use the expression 'for flow in traffic_matrix'
        """
        return iter(self.flows())

    def __len__(self):
        """
        Return the number of OD pairs of the matrix. Use the expression
        'len(traffic_matrix)'

        Returns
        -------
        len : int
            The number of OD pairs
        """
        return len(self.flows())

    def __contains__(self, item):
        """
        Test whether a specific OD flow is in the matrix or not. Use the
        expression '(origin, destination) in traffic_matrix'
        """
        origin, destination = item
        return origin in self.flow and destination in self.flow[origin]

    def __getitem__(self, key):
        """
        Return the traffic volume of a specific flow of the matrix. Use the
        expression 'volume = traffic_matrix[(origin, destination)]'
        """
        origin, destination = key
        return self.flow[origin][destination]

    def __setitem__(self, key, value):
        """
        Sets the traffic volume of a specific flow of the matrix. Use the
        expression 'traffic_matrix[(origin, destination)] = volume'
        """
        origin, destination = key
        if not origin in self.flow:
            self.flow[origin] = {}
        self.flow[origin][destination] = value

    def __delitem__(self, key):
        """
        Delete a specific flow from the matrix. Use the
        expression 'del traffic_matrix[(u, v)]'
        """
        origin, destination = key
        del self.flow[origin][destination]
        if len(self.flow[origin]) == 0:
            del self.flow[origin]

    def flows(self):
        """
        Return the flows of the traffic matrix

        Returns
        -------
        flows : dict
            A dictionary of all traffic volumes keyed by OD pair
        """
        return {(o, d): self.flow[o][d]
                for o in self.flow for d in self.flow[o] if o != d}

    def od_pairs(self):
        """
        Return all OD pairs of the traffic matrix

        Returns
        -------
        od_pairs : list
            A list of OD pairs. Each OD pair is expressed as an
            (origin, destination) tuple
        """
        return [(o, d) for o in self.flow for d in self.flow[o] if o != d]

    def add_flow(self, origin, destination, volume):
        """
        Add a flow to the traffic matrix

        Parameters
        ----------
        origin : any hashable type
            The origin node
        destination : any hashable type
            The destination node
        volume : float
            The traffic volume
        """
        if origin not in self.flow:
            self.flow[origin] = {}
        self.flow[origin][destination] = volume

    def pop_flow(self, origin, destination):
        """
        Pop a flow from the traffic matrix and return the volume of the flow
        removed. If the flow to remove does not exist, a KeyError is raised.

        Parameters
        ----------
        origin : any hashable type
            The origin node
        destination : any hashable type
            The destination node

        Raises
        ------
        KeyError:
            if there is no flow from the given origin to the given destination

        Returns
        -------
        volume : float
            The volume of the flow popped from the matrix
        """
        if origin not in self.flow or destination not in self.flow[origin]:
            raise KeyError('There is no flow from %s to %s'
                           % (str(origin), str(destination)))
        return self.flow[origin].pop(destination)


class TrafficMatrixSequence(object):
    """
    Class representing a sequence of traffic matrices.

    Parameters
    ----------
    interval : float or int, optional
        The time interval elapsed between subsequent traffic matrices of the
        sequence
    t_unit : str, optional
        The unit of the interval value (e.g. 'sec' or 'min')
    """

    def __init__(self, interval=None, t_unit='min'):
        """
        Initialize the traffic matrix sequence

        Parameters
        ----------
        interval : float, optional
            The time interval between subsequent traffic matrices of the
            sequence
        t_unit : str, optional
            The time unit of the time interval
        """
        self.attrib = {}
        if interval is not None:
            if not t_unit in time_units:
                raise ValueError("The t_unit argument is not valid")
            self.attrib['interval'] = interval
            self.attrib['t_unit'] = t_unit
        self.matrix = []
        return

    def __iter__(self):
        """
        Iterates over the matrices of the sequence. Use the expression
        'for traffic_matrix in traffic_matrix_sequence'
        """
        return iter(self.matrix)

    def __len__(self):
        """
        Return the number of traffic matrices of the sequence. Use the
        expression 'len(traffic_matrix_sequence)'
        """
        return len(self.matrix)

    def __getitem__(self, key):
        """
        Return the traffic matrix at a specific index of the sequence. Use the
        expression 'traffic_matrix = traffic_matrix_sequence[i]'
        """
        return self.matrix[key]

    def __setitem__(self, key, value):
        """
        Add/edit the traffic matrix at a specific index of the sequence. Use
        the expression 'traffic_matrix_sequence[i] = traffic_matrix'
        """
        self.matrix[key] = value

    def __delitem__(self, key):
        """
        Remove the traffic matrix at a specific index of the sequence. Use the
        expression 'del traffic_matrix_sequence[i]'
        """
        del self.matrix[key]

    def insert(self, i, tm):
        """
        Insert a traffic matrix in the sequence at a specified position

        Parameters
        ----------
        i : int
            The position at which the matrix is inserted

        tm : TrafficMatrix
            The traffic matrix to insert
        """
        self.matrix.insert(i, tm)

    def append(self, tm):
        """
        Append a traffic matrix at the end of the sequence

        Parameters
        ----------
        tm : TrafficMatrix
            The traffic matrix to append
        """
        self.matrix.append(tm)

    def get(self, i):
        """
        Return a specific traffic matrix in a specific position of the sequence

        Parameters
        ----------
        i : int
            The index of the traffic matrix

        Returns
        -------
        tm : TrafficMatrix
        """
        return self.matrix[i]


    def pop(self, i):
        """
        Removes the traffic matrix in a specific position of the sequence

        Parameters
        ----------
        i : int
            The index of the traffic matrix to remove

        Raises
        ------
        IndexError : if list is empty or index is out of range.

        Returns
        -------
        tm : TrafficMatrix
            The TrafficMatrix popped from the sequence

        Examples
        --------
        >>> import fnss
        >>> tms = fnss.TrafficMatrixSequence()
        >>> tm = TrafficMatrix()
        >>> tms.append(tm)
        >>> tms.remove(tm)
        """
        self.matrix.pop(i)


# We assume that links are full duplex, if undirected
def static_traffic_matrix(topology, mean, stddev, max_u=0.9,
                          origin_nodes=None, destination_nodes=None):
    """
    Return a TrafficMatrix object, i.e. a single traffic matrix, representing
    the traffic volume exchanged over a network at a specific point in time

    This matrix is generated by assigning traffic volumes drawn from a
    lognormal distribution and assigned to specific origin-destination pairs
    using the Ranking Metrics Heuristic method proposed by Nucci et al. [1]_

    Parameters
    ----------
    topology : topology
        The topology for which the traffic matrix is calculated. This topology
        can either be directed or undirected. If it is undirected, this
        function assumes that all links are full-duplex.

    mean : float
        The mean volume of traffic among all origin-destination pairs

    stddev : float
        The standard deviation of volumes among all origin-destination pairs.

    max_u : float, optional
        Represent the max link utilization. If specified, traffic volumes are
        scaled so that the most utilized link of the network has an utilization
        equal to max_u. If None, volumes are not scaled, but in this case links
        may end up with an utilization factor greater than 1.0

    origin_nodes : list, optional
        A list of all nodes which can be traffic sources. If not specified,
        all nodes of the topology are traffic sources

    destination_nodes : list, optional
        A list of all nodes which can be traffic destinations. If not
        specified, all nodes of the topology are traffic destinations

    Returns
    -------
    tm : TrafficMatrix

    References
    ----------
    .. [1] Nucci et al., The problem of synthetically generating IP traffic
       matrices: initial recommendations, ACM SIGCOMM Computer Communication
       Review, 35(3), 2005
    """
    try:
        mean = float(mean)
        stddev = float(stddev)
    except ValueError:
        raise ValueError('mean and stddev must be of type float')
    if mean < 0 or stddev < 0:
        raise ValueError('mean and stddev must be not negative')
    topology = topology.copy() if topology.is_directed() \
               else topology.to_directed()
    volume_unit = topology.graph['capacity_unit']
    mu = log(mean ** 2 / sqrt(stddev ** 2 + mean ** 2))
    sigma = sqrt(log((stddev ** 2 / mean ** 2) + 1))
    if origin_nodes is None and destination_nodes is None:
        od_pairs = od_pairs_from_topology(topology)
    else:
        all_nodes = topology.nodes()
        origins = origin_nodes or all_nodes
        destinations = destination_nodes or all_nodes
        od_pairs = [(o, d) for o in origins for d in destinations if o != d]
    nr_pairs = len(od_pairs)
    volumes = sorted(lognormal(mu, sigma, size=nr_pairs))
    # volumes = sorted([lognormvariate(mu, sigma) for _ in range(nr_pairs)])
    if any(isinf(vol) for vol in volumes):
        raise ValueError('Some volumes are too large to be handled by a '\
                         'float type. Set a lower value of mu and try again.')
    sorted_od_pairs = __ranking_metrics_heuristic(topology, od_pairs)
    # check if the matrix matches and scale if needed
    assignments = dict(zip(sorted_od_pairs, volumes))
    if max_u is not None:
        if origin_nodes is not None:
            shortest_path = dict(
                    (node, nx.single_source_dijkstra_path(topology,
                                                          node,
                                                          weight='weight'))
                    for node in origin_nodes)
            # remove OD pairs not connected
            for o, d in itertools.product(shortest_path, destinations):
                if o != d and d not in shortest_path[o]:
                    od_pairs.remove((o, d))
        else:
            shortest_path = dict(nx.all_pairs_dijkstra_path(topology,
                                                            weight='weight'))
        for u, v in topology.edges():
            topology.adj[u][v]['load'] = 0.0
        # Find max u
        for o, d in od_pairs:
            path = shortest_path[o][d]
            if len(path) > 1:
                for u, v in zip(path[:-1], path[1:]):
                    topology.adj[u][v]['load'] += assignments[(o, d)]
        # Calculate scaling
        current_max_u = max((float(topology.adj[u][v]['load']) \
                             / float(topology.adj[u][v]['capacity'])
                             for u, v in topology.edges()))
        norm_factor = max_u / current_max_u
        for od_pair in assignments:
            assignments[od_pair] *= norm_factor

    # write to traffic matrix
    traffic_matrix = TrafficMatrix(volume_unit=volume_unit)
    for (o, d), flow in assignments.items():
        traffic_matrix.add_flow(o, d, flow)
    return traffic_matrix


def stationary_traffic_matrix(topology, mean, stddev, gamma, log_psi, n,
                              max_u=0.9,
                              origin_nodes=None, destination_nodes=None):
    """
    Return a stationary sequence of traffic matrices.

    The sequence is generated by first generating a single matrix assigning
    traffic volumes drawn from a lognormal distribution and assigned to
    specific origin-destination pairs using the Ranking Metrics Heuristic
    method proposed by Nucci et al. [2]_. Then, all matrices of the sequence
    are generated by adding zero-mean normal fluctuation in the traffic
    volumes. This process was originally proposed by [2]_

    Stationary sequences of traffic matrices are generally suitable for
    modeling network traffic over short periods (up to 1.5 hours). Over longer
    periods, real traffic exhibits diurnal patterns and they are better
    modelled by cyclostationary sequences

    Parameters
    ----------
    topology : topology
        The topology for which the traffic matrix is calculated. This topology
        can either be directed or undirected. If it is undirected, this
        function assumes that all links are full-duplex.

    mean : float
        The mean volume of traffic among all origin-destination pairs

    stddev : float
        The standard deviation of volumes among all origin-destination pairs.

    gamma : float
        Parameter expressing relation between mean and standard deviation of
        traffic volumes of a specific flow over the time

    log_psi : float
        Parameter expressing relation between mean and standard deviation of
        traffic volumes of a specific flow over the time

    n : int
        Number of matrices in the sequence

    max_u : float, optional
        Represent the max link utilization. If specified, traffic volumes are
        scaled so that the most utilized link of the network has an utilization
        equal to max_u. If None, volumes are not scaled, but in this case links
        may end up with an utilization factor greater than 1.0

    origin_nodes : list, optional
        A list of all nodes which can be traffic sources. If not specified
        all nodes of the topology are traffic sources

    destination_nodes : list, optional
        A list of all nodes which can be traffic destinations. If not specified
        all nodes of the topology are traffic destinations

    Returns
    -------
    tms : TrafficMatrixSequence

    References
    ----------
    .. [2] Nucci et al., The problem of synthetically generating IP traffic
       matrices: initial recommendations, ACM SIGCOMM Computer Communication
       Review, 35(3), 2005
    """
    tm_sequence = TrafficMatrixSequence()
    static_tm = static_traffic_matrix(topology, mean, stddev, max_u=None,
                                      origin_nodes=origin_nodes,
                                      destination_nodes=destination_nodes)
    volume_unit = static_tm.attrib['volume_unit']
    mean_dict = static_tm.flows()
    psi = exp(log_psi)
    if psi == 0.0:
        raise ValueError("The value of log_psi provided is too small and "
                         "causes psi=0.0, which makes the standard deviation "
                         "of random fluctuation to become infinite. Try with "
                         "a greater value of log_psi")
    std_dict = {(o, d): (m / psi) ** (1.0 / gamma)
                for (o, d), m in mean_dict.items()}
    if any(isinf(std) for std in std_dict.values()):
        raise ValueError("The value of log_psi or gamma provided are too "
                         "small and causes the standard deviation of random "
                         "fluctuations to become infinite. Try with a greater "
                         "value of log_psi and/or gamma")
    flows = {}
    for o, d in mean_dict:
        # Implementation without Numpy:
        # flows[(o, d)] = [max([0, normalvariate(mean_dict[(o, d)],
        #                std_dict[(o, d)])]) for _ in range(n)]
        flows[(o, d)] = [max((0, normal(mean_dict[(o, d)], std_dict[(o, d)])))\
                         for _ in range(n)]

    for i in range(n):
        traffic_marix = TrafficMatrix(volume_unit=volume_unit)
        for o, d in mean_dict:
            traffic_marix.add_flow(o, d, flows[(o, d)][i])
        tm_sequence.append(traffic_marix)
    if max_u is not None:
        if origin_nodes is not None:
            shortest_path = dict(
                    (node, nx.single_source_dijkstra_path(topology,
                                                          node,
                                                          weight='weight'))
                    for node in origin_nodes)
        else:
            shortest_path = dict(nx.all_pairs_dijkstra_path(topology,
                                                            weight='weight'))
        current_max_u = max((max(link_loads(topology,
                                            tm_sequence.get(i),
                                            shortest_path
                                            ).values())
                             for i in range(n)))
        norm_factor = max_u / current_max_u
        for i in range(n):
            for o, d in mean_dict:
                tm_sequence.matrix[i].flow[o][d] *= norm_factor
    return tm_sequence



def sin_cyclostationary_traffic_matrix(topology, mean, stddev, gamma, log_psi,
                                       delta=0.2, n=24, periods=1, max_u=0.9,
                                       origin_nodes=None,
                                       destination_nodes=None):
    """
    Return a cyclostationary sequence of traffic matrices, where traffic
    volumes evolve over time as sin waves.

    The sequence is generated by first generating a single matrix assigning
    traffic volumes drawn from a lognormal distribution and assigned to
    specific origin-destination pairs using the Ranking Metrics Heuristic
    method proposed by Nucci et al. [3]_. Then, all matrices of the sequence
    are generated by adding zero-mean normal fluctuation in the traffic
    volumes. Finally, traffic volumes are multiplied by a sin function with
    unitary mean to model periodic fluctuations.

    This process was originally proposed by [3]_.

    Cyclostationary sequences of traffic matrices are generally suitable for
    modeling real network traffic over long periods, up to several days. In
    fact, real traffic exhibits diurnal patterns well modelled by
    cyclostationary sequences.

    Parameters
    ----------
    topology : topology
        The topology for which the traffic matrix is calculated. This topology
        can either be directed or undirected. If it is undirected, this
        function assumes that all links are full-duplex.

    mean : float
        The mean volume of traffic among all origin-destination pairs

    stddev : float
        The standard deviation of volumes among all origin-destination pairs.

    gamma : float
        Parameter expressing relation between mean and standard deviation of
        traffic volumes of a specific flow over the time

    log_psi : float
        Parameter expressing relation between mean and standard deviation of
        traffic volumes of a specific flow over the time

    delta : float [0, 1]
        A parameter indicating the intensity of variation of traffic volumes
        over a period. Specifically, let x be the mean volume over a specific
        OD pair, the minimum and maximum traffic volumes for that OD pair
        (excluding random fluctuations) are respectively :math:`x*(1 - delta)`
        and :math:`x*(1 + delta)`

    n : int
        Number of traffic matrices per period. For example, if it is desired to
        model traffic varying cyclically over a 24 hour period, and n is set to
        24, therefore, the time interval between subsequent traffic matrices is
        is 1 hour.

    periods : int
        Number of periods. In total the sequence is composed of
        :math:`n * periods` traffic matrices.

    max_u : float, optional
        Represent the max link utilization. If specified, traffic volumes are
        scaled so that the most utilized link of the network has an utilization
        equal to max_u. If None, volumes are not scaled, but in this case links
        may end up with an utilization factor greater than 1.0

    origin_nodes : list, optional
        A list of all nodes which can be traffic sources. If not specified
        all nodes of the topology are traffic sources

    destination_nodes : list, optional
        A list of all nodes which can be traffic destinations. If not specified
        all nodes of the topology are traffic destinations

    Returns
    -------
    tms : TrafficMatrixSequence

    References
    ----------
    .. [3] Nucci et al., The problem of synthetically generating IP traffic
       matrices: initial recommendations, ACM SIGCOMM Computer Communication
       Review, 35(3), 2005
    """
    tm_sequence = TrafficMatrixSequence()
    static_tm = static_traffic_matrix(topology, mean, stddev, max_u=None,
                                      origin_nodes=origin_nodes,
                                      destination_nodes=destination_nodes)
    volume_unit = static_tm.attrib['volume_unit']
    mean_dict = static_tm.flows()
    psi = exp(log_psi)
    if psi == 0.0:
        raise ValueError("The value of log_psi provided is too small and "
                         "causes psi=0.0, which makes the standard deviation "
                         "of random fluctuation to become infinite. Try with "
                         "a greater value of log_psi")
    std_dict = {(o, d): (m / psi) ** (1.0 / gamma)
                for (o, d), m in mean_dict.items()}
    print(std_dict.values())
    if any(isinf(std) for std in std_dict.values()):
        raise ValueError("The value of log_psi or gamma provided are too "
                         "small and causes the standard deviation of random "
                         "fluctuations to become infinite. Try with a greater "
                         "value of log_psi and/or gamma")
    od_pairs = static_tm.od_pairs()
    for _ in range(periods):
        for i in range(n):
            tm = TrafficMatrix(volume_unit=volume_unit)
            for o, d in od_pairs:
                volume = static_tm[(o, d)] * (1 + delta * sin((2 * pi * i) / n))
                # Implementation without Numpy
                # volume = max([0, normalvariate(volume, std_dict[(o, d)])])
                volume = max((0, normal(volume, std_dict[(o, d)])))
                tm.add_flow(o, d, volume)
            tm_sequence.append(tm)

    if max_u is not None:
        if origin_nodes is not None:
            shortest_path = dict(
                    (node, nx.single_source_dijkstra_path(topology,
                                                          node,
                                                          weight='weight'))
                    for node in origin_nodes)
        else:
            shortest_path = dict(nx.all_pairs_dijkstra_path(topology,
                                                            weight='weight'))
        current_max_u = max((max(link_loads(topology,
                                            tm_sequence.get(i),
                                            shortest_path
                                            ).values())
                             for i in range(n * periods)))
        norm_factor = max_u / current_max_u
        for i in range(n * periods):
            for o, d in mean_dict:
                tm_sequence.matrix[i].flow[o][d] *= norm_factor
    return tm_sequence


def __ranking_metrics_heuristic(topology, od_pairs=None):
    """
    Sort OD pairs of a topology according to the Ranking Metrics Heuristics
    method

    Parameters
    ----------
    topology : Topology or DirectedTopology
        The topology
    od_pairs : list, optional
        The OD pairs to be ranked (must be a subset of the OD pairs of the
        topology). If None, then the heuristic is calculated for all the OD
        pairs of the topology

    Returns
    -------
    od_pairs : list
        The sorted list of OD pairs
    """
    # Ranking Metrics Heuristic
    if od_pairs is None:
        od_pairs = od_pairs_from_topology(topology)

    fan_in, fan_out = fan_in_out_capacities(topology)
    degree = topology.degree()
    min_capacity = {(u, v): min(fan_out[u], fan_in[v]) for u, v in od_pairs}
    min_degree = {(u, v): min(degree[u], degree[v]) for u, v in od_pairs}

    # NFUR calculation is expensive, so before calculating it, the code
    # checks if it is really needed, i.e. if there are ties after capacity
    # and degree sorting
    cap_deg_pairs = [(min_capacity[(u, v)], min_degree[(u, v)])
                     for u, v in od_pairs]
    nfur_required = any((val > 1 for val in Counter(cap_deg_pairs).values()))
    if not nfur_required:
        # Sort all OD_pairs
        return sorted(od_pairs, key=lambda od_pair: (min_capacity[od_pair],
                                                     min_degree[od_pair]))
    # if NFUR is required we calculate it. If fast is True, this function
    # returns the betweenness centrality rather than the NFUR.
    # Use betweenness centrality instead of NFUR if the topology is not trivial
    # for scalability reasons.
    # The threshold of 300 is a conservative value which allows fast execution
    # on most machines.
    parallelize = (topology.number_of_edges() > 100)
    fast = (topology.number_of_edges() > 300)
    nfur = __calc_nfur(topology, fast, parallelize)
    # Note: here we use the opposite of max rather than the inverse of max
    # (which is the formulation of the paper) because we only need to rank
    # in reverse order the max of NFURs. Since all NFURs are >=0,
    # using the opposite yields the same results as the inverse, but there
    # is no risk of incurring in divisions by 0.
    max_inv_nfur = {(u, v):-max(nfur[u], nfur[v]) for u, v in od_pairs}
    # Sort all OD_pairs
    return sorted(od_pairs, key=lambda od_pair: (min_capacity[od_pair],
                                                 min_degree[od_pair],
                                                 max_inv_nfur[od_pair]))


def __calc_nfur(topology, fast, parallelize=True):
    """
    Calculate the Number of Flows under Failure (NFUR) for all nodes of a
    topology

    Parameters
    ----------
    topology : Topology or DirectedTopology
        The topology
    fast : bool
        If True returns betweenness centrality instead of NFUR
    parallelize : bool
        If True, spawns as many processes as the number of cores of the machine
        using the map-reduce algorithm. It is always recommended unless the
        topology is very small. If *fast* parameter is True, this option is
        ignored, as betweenness centrality calculation cannot be parallelized.

    Returns
    -------
    nfur : dict
        A dictionary of the NFURs of the topology keyed by node. If fast is
        True, returns betweenness centrality instead.

    Notes
    -----
    The time complexity of the calculation of NFUR grows linearly with the
    number of links. A topology with thousands of links is likely to take hours
    to compute on commodity hardware. For this reason, this function can spawn
    as many processes as the number of cores of the machine on which it runs
    and parallelizes the task with a map-reduce algorithm.
    """
    # Note: The NFUR calculation doesn't scale because I need to calc betw for
    # each edge removed. With many nodes and edges, takes very long. The
    # parallelization reduced the time but it can still be very long
    betw = nx.betweenness_centrality(topology, normalized=False,
                                     weight='weight')
    if fast:
        return betw
    edges = topology.edges()
    if not parallelize:
        # execute the NFUR calculation in one single process
        # Recommended only if the size of the topology is so small that the
        # overhead of creating new processes overcomes the performance gains
        # achieved by splitting the calculation
        return __nfur_func(topology, edges, betw)
    try:
        processes = mp.cpu_count()
    except NotImplementedError:
        processes = 32  # upper bound of number of cores on a commodity server
    pool = mp.Pool(processes)
    # map operation
    edges_chunks = util.split_list(edges, len(edges) // processes)
    args = [(__nfur_func, (topology, chunk, betw)) for chunk in edges_chunks]
    result = pool.map(util.map_func, args)
    # reduce operation
    return {v: max((result[i][v] for i in range(len(result)))) for v in betw}

def __nfur_func(topology, edges, betweenness):
    """
    Calculate NFUR on a specific set of edges

    Parameters
    ----------
    topology : Topology
        The topology
    edges : list
        The list of edges (subset of topology edges)
    betweenness : dict
        The betweeness centrality of the topology, keyed by node

    Returns
    -------
    nfur : dict
        NFUR values keyed by node, only relative to failures of the specified
        edges
    """
    nfur = betweenness.copy()
    topology = topology.copy()
    for u, v in edges:
        edge_attr = topology.adj[u][v]
        topology.remove_edge(u, v)
        betw = nx.betweenness_centrality(topology, normalized=False,
                                         weight='weight')
        for node in betw.keys():
            if betw[node] > nfur[node]:
                nfur[node] = betw[node]
        topology.add_edge(u, v, **edge_attr)
    return nfur


# Note: Calling networkx's all_pairs_shortest_path does not return multiple
# paths with same cost (and apparently doesn't even select path randomly,
# but selects the next hop with lowest ID).
def validate_traffic_matrix(topology, traffic_matrix, validate_load=False):
    """
    Validate whether a given traffic matrix and given topology are compatible.

    Returns True if they are compatible, False otherwise

    This validation includes validating whether the origin-destination pairs of
    the traffic matrix are coincide with or are a subset of the
    origin-destination pairs of the topology. Optionally, this function can
    verify if the volumes of the traffic matrix are compatible too, i.e. if at
    any time, no link has an utilization greater than 1.0.

    Parameters
    ----------
    topology : topology
        The topology agains which the traffic matrix is validated
    tm : TrafficMatrix or TrafficMatrixSequence
        The traffic matrix (or sequence of) to be validated
    validate_load : bool, optional
        Specify whether load compatibility has to be validated or not.
        Default value is False

    Returns
    -------
    is_valid : bool
        True if the topology and the traffic matrix are compatible,
        False otherwise
    """
    if isinstance(traffic_matrix, TrafficMatrix):
        matrices = [traffic_matrix]
    elif isinstance(traffic_matrix, TrafficMatrixSequence):
        matrices = traffic_matrix.matrix
    else:
        raise ValueError('tm must be either a TrafficMatrix or a '\
                         ' TrafficMatrixSequence object')

    topology = topology.copy() if topology.is_directed() \
                               else topology.to_directed()

    od_pairs_topology = od_pairs_from_topology(topology)
    if validate_load:
        shortest_path = dict(nx.all_pairs_dijkstra_path(topology,
                                                        weight='weight'))
    for matrix in matrices:
        od_pairs_tm = matrix.od_pairs()
        # verify that OD pairs in TM are equal or subset of topology
        if not all(((o, d) in od_pairs_topology for o, d in od_pairs_tm)):
            return False
        if validate_load:
            for u, v in topology.edges():
                topology.adj[u][v]['load'] = 0
            capacity_unit = capacity_units[topology.graph['capacity_unit']]
            volume_unit = capacity_units[matrix.attrib['volume_unit']]
            norm_factor = float(volume_unit) / float(capacity_unit)
            for o, d in od_pairs_tm:
                path = shortest_path[o][d]
                if len(path) <= 1:
                    continue
                for u, v in zip(path[:-1], path[1:]):
                    topology.adj[u][v]['load'] += matrix.flow[o][d]
            max_u = max((norm_factor * float(topology.adj[u][v]['load']) \
                         / float(topology.adj[u][v]['capacity'])
                         for u, v in topology.edges()))
            if max_u > 1.0: return False
    return True


def link_loads(topology, traffic_matrix, routing_matrix=None, ecmp=False):
    """
    Calculate link utilization given a traffic matrix.

    Return a dictionary mapping for each link of a topology, the relative link
    utilization (i.e. traffic volume divided by link capacity) given a traffic
    matrix. The keys of the dictionary are (u, v) tuple where u and v are
    respectively the source and destination nodes of the link. The values are
    float values between 0 and 1. A zero value means that the link is not
    utilized, while a one value means that the link is saturated.

    Link utilizations are calculated assuming that all traffic is routed
    following the shortest path from origin to destination, calculated with the
    Dijkstra algorithm. If the topology is annotated with link weights, they
    are used for the shortest path calculation. Otherwise hop count is used.

    Parameters
    ----------
    topology : topology
        The topology whose link utilization is calculated. This topology must
        be annotate with at least link capacity. If it also presents link
        weights, those are used for shortest paths calculation.
    tm : TrafficMatrix
        The traffic matrix associated to the topology.
    routing_matrix : dict of dicts
        The routing matrix used by the traffic. This matrix is a dictionary of
        dictionaries, where the keys of the root dictionary are the origin
        nodes, the keys of the nested dictionary are the destination nodes and
        the values of the nested dictionary are lists of nodes on the path
        from origin to destination (both included). For example, if the
        path from node 1 to node 4 is 1 -> 2 -> 3 -> 4, then
        routing_matrix[1][4] = [1, 2, 3, 4].
        If ecmp is set to True, the values of the nested dictionary are lists
        of lists of nodes, each representing a path, among which the load will
        be equally divided.
        The networkx all_pairs_dijkstra_path function returns shortest paths
        in this format.
        If this parameter is None, then Dijkstra shortest paths are used.
    ecmp: bool
        Enables the usage of Equal-Cost Multi Path Routing.

    Returns
    -------
    link_loads : dict
        A dictionary of link loads keyed by link

    """
    topology = topology.copy() if topology.is_directed() \
                               else topology.to_directed()
    capacity_unit = capacity_units[topology.graph['capacity_unit']]
    volume_unit = capacity_units[traffic_matrix.attrib['volume_unit']]
    norm_factor = float(volume_unit) / float(capacity_unit)
    if routing_matrix == None:
        routing_matrix = dict(nx.all_pairs_dijkstra_path(topology,
                                                         weight='weight'))
    for u, v in topology.edges():
        topology.adj[u][v]['load'] = 0
    od_pairs = traffic_matrix.od_pairs()

    def process_path(path, number_of_paths=1):
        if len(path) <= 1:
            return
        for u, v in zip(path[:-1], path[1:]):
            if not ecmp:
                topology.adj[u][v]['load'] += traffic_matrix.flow[o][d]
            else:
                topology.adj[u][v]['load'] += \
                            traffic_matrix.flow[o][d] / float(number_of_paths)

    for o, d in od_pairs:
        try:
            path = routing_matrix[o][d]
        except KeyError:
            raise ValueError('Cannot calculate link loads. There is no route' \
                             'from node %s to node %s' % (str(o), str(d)))
        if not ecmp:
            process_path(path)
        else:
            for p in path:
                process_path(p, len(path))

    return {(u, v): norm_factor * float(topology.adj[u][v]['load']) \
            / float(topology.adj[u][v]['capacity'])
            for u, v in topology.edges()}


def read_traffic_matrix(path, encoding='utf-8'):
    """
    Parses a traffic matrix from a traffic matrix XML file. If the XML file
    contains more than one traffic matrix, it returns a TrafficMatrixSequence
    object, otherwise a TrafficMatrixObject.

    Parameters
    ----------
    path: str
        The path of the XML file to parse
    encoding : str, optional
        The encoding of the file

    Returns
    -------
    tm : TrafficMatrix or TrafficMatrixSequence
    """
    def parse_single_matrix(head):
        """
        Parses a single traffic matrix from the XML file
        """
        traffic_matrix = TrafficMatrix()
        for prop in head.findall('property'):
            name = prop.attrib['name']
            value = util.xml_cast_type(prop.attrib['type'], prop.text)
            if name == 'volume_unit' and value not in capacity_units:
                raise ET.ParseError(\
                                'Invalid volume_unit property in time node')
            traffic_matrix.attrib[name] = value
        for origin in head.findall('origin'):
            o = util.xml_cast_type(origin.attrib['id.type'], origin.attrib['id'])
            for destination in origin.findall('destination'):
                d = util.xml_cast_type(destination.attrib['id.type'],
                                   destination.attrib['id'])
                volume = float(destination.text)
                traffic_matrix.add_flow(o, d, volume)
        return traffic_matrix
    tree = ET.parse(path)
    head = tree.getroot()
    matrix_type = head.attrib['type']
    if matrix_type == 'single':
        traffic_matrix = parse_single_matrix(head.find('time'))
    elif matrix_type == 'sequence':
        traffic_matrix = TrafficMatrixSequence()
        for prop in head.findall('property'):
            name = prop.attrib['name']
            value = util.xml_cast_type(prop.attrib['type'], prop.text)
            traffic_matrix.attrib[name] = value
        for matrix in head.findall('time'):
            traffic_matrix.append(parse_single_matrix(matrix))
    else:
        raise ET.ParseError('Invalid TM type attribute in XML file')
    return traffic_matrix


def write_traffic_matrix(traffic_matrix, path, encoding='utf-8',
                         prettyprint=True):
    """
    Write a TrafficMatrix or a TrafficMatrixSequence object to an XML file.
    This function can be use to either persistently store a traffic matrix for
    later use or to export it to an FNSS adapter for a simulator or an API for
    another programming language.

    Parameters
    ----------
    traffic_matrix : TrafficMatrix or TrafficMatrixSequence
        The traffic matrix to save
    path : str
        The path where the file will be saved
    encoding : str, optional
        The desired encoding of the output file
    prettyprint : bool, optional
        Specify whether the XML file should be written with indentation for
        improved human readability
    """
    head = ET.Element("traffic-matrix")
    if isinstance(traffic_matrix, TrafficMatrix):
        head.attrib['type'] = 'single'
        matrices = [traffic_matrix]
    elif isinstance(traffic_matrix, TrafficMatrixSequence):
        for name, value in traffic_matrix.attrib:
            prop = ET.SubElement(head, "property")
            prop.attrib['name'] = str(name)
            prop.attrib['type'] = util.xml_type(value)
            prop.text = str(value)
        head.attrib['type'] = 'sequence'
        matrices = traffic_matrix.matrix
    else:
        raise ValueError('traffic_matrix parameter must be either a ' /
                         'TrafficMatrix or a TrafficMatrixSequence instance')
    for matrix in matrices:
        time = ET.SubElement(head, "time")
        time.attrib['seq'] = str(matrices.index(matrix))
        for name, value in matrix.attrib.items():
            prop = ET.SubElement(time, "property")
            prop.attrib['name'] = str(name)
            prop.attrib['type'] = util.xml_type(value)
            prop.text = str(value)
        for o in matrix.flow:
            origin = ET.SubElement(time, "origin")
            origin.attrib['id'] = str(o)
            origin.attrib['id.type'] = util.xml_type(o)
            for d in matrix.flow[o]:
                volume = matrix.flow[o][d]
                destination = ET.SubElement(origin, "destination")
                destination.attrib['id'] = str(d)
                destination.attrib['id.type'] = util.xml_type(d)
                destination.text = str(volume)
    if prettyprint:
        util.xml_indent(head)
    ET.ElementTree(head).write(path, encoding=encoding)
