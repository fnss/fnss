"""Functions to generate random topologies according to a number of models.

The generated topologies are either Topology or DirectedTopology objects.
"""
import math
import random

import networkx as nx

from fnss.util import random_from_pdf
from fnss.topologies.topology import Topology


__all__ = [
    'erdos_renyi_topology',
    'waxman_1_topology',
    'waxman_2_topology',
    'barabasi_albert_topology',
    'extended_barabasi_albert_topology',
    'glp_topology'
          ]

def erdos_renyi_topology(n, p, seed=None, fast=False):
    r"""Return a random graph :math:`G_{n,p}` (Erdos-Renyi graph, binomial
    graph).

    Chooses each of the possible edges with probability p.

    Parameters
    ----------
    n : int
        The number of nodes.
    p : float
        Probability for edge creation.
    seed : int, optional
        Seed for random number generator (default=None).
    fast : boolean, optional
        Uses the algorithm proposed by [3]_, which is faster for small p

    References
    ----------
    .. [1] P. Erdos and A. Renyi, On Random Graphs, Publ. Math. 6, 290 (1959).
    .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
    .. [3] Vladimir Batagelj and Ulrik Brandes,
       "Efficient generation of large random networks",
       Phys. Rev. E, 71, 036113, 2005.
    """
    # validate input parameters
    if not isinstance(n, int) or n < 0:
        raise ValueError('n must be a positive integer')
    if p > 1 or p < 0:
        raise ValueError('p must be a value in (0,1)')
    if fast:
        G = Topology(nx.fast_gnp_random_graph(n, p, seed=seed))
    else:
        G = Topology(nx.gnp_random_graph(n, p, seed=seed))
    G.name = "erdos_renyi_topology(%s, %s)" % (n, p)
    G.graph['type'] = 'er'
    return G


def waxman_1_topology(n, alpha=0.4, beta=0.1, L=1.0,
                      distance_unit='Km', seed=None):
    r"""
    Return a Waxman-1 random topology.

    The Waxman-1 random topology models assigns link between nodes with
    probability

    .. math::
            p = \alpha*exp(-d/(\beta*L)).

    where the distance *d* is chosen randomly in *[0,L]*.

    Parameters
    ----------
    n : int
        Number of nodes
    alpha : float
        Model parameter chosen in *(0,1]* (higher alpha increases link density)
    beta : float
        Model parameter chosen in *(0,1]* (higher beta increases difference
        between density of short and long links)
    L : float
        Maximum distance between nodes.
    seed : int, optional
        Seed for random number generator (default=None).

    Returns
    -------
    G : Topology

    Notes
    -----
    Each node of G has the attributes *latitude* and *longitude*. These
    attributes are not expressed in degrees but in *distance_unit*.

    Each edge of G has the attribute *length*, which is also expressed in
    *distance_unit*.

    References
    ----------
    .. [1]  B. M. Waxman, Routing of multipoint connections.
       IEEE J. Select. Areas Commun. 6(9),(1988) 1617-1622.
    """
    # validate input parameters
    if not isinstance(n, int) or n <= 0:
        raise ValueError('n must be a positive integer')
    if alpha > 1 or alpha <= 0 or beta > 1 or beta <= 0:
        raise ValueError('alpha and beta must be float values in (0,1]')
    if L <= 0:
        raise ValueError('L must be a positive number')
    if seed is not None:
        random.seed(seed)

    G = Topology(type='waxman_1', distance_unit=distance_unit)

    G.name = "waxman_1_topology(%s, %s, %s, %s)" % (n, alpha, beta, L)
    G.add_nodes_from(range(n))
    nodes = list(G.nodes())
    while nodes:
        u = nodes.pop()
        for v in nodes:
            d = L * random.random()
            if random.random() < alpha * math.exp(-d / (beta * L)):
                G.add_edge(u, v, length=d)
    return G


def waxman_2_topology(n, alpha=0.4, beta=0.1, domain=(0, 0, 1, 1),
                      distance_unit='Km', seed=None):
    r"""Return a Waxman-2 random topology.

    The Waxman-2 random topology models place n nodes uniformly at random
    in a rectangular domain. Two nodes u, v are connected with a link
    with probability

    .. math::
            p = \alpha*exp(-d/(\beta*L)).

    where the distance *d* is the Euclidean distance between the nodes u and v.
    and *L* is the maximum distance between all nodes in the graph.


    Parameters
    ----------
    n : int
        Number of nodes
    alpha : float
        Model parameter chosen in *(0,1]* (higher alpha increases link density)
    beta : float
        Model parameter chosen in *(0,1]* (higher beta increases difference
        between density of short and long links)
    domain : tuple of numbers, optional
         Domain size (xmin, ymin, xmax, ymax)
    seed : int, optional
        Seed for random number generator (default=None).

    Returns
    -------
    G : Topology

    Notes
    -----
    Each edge of G has the attribute *length*

    References
    ----------
    .. [1]  B. M. Waxman, Routing of multipoint connections.
       IEEE J. Select. Areas Commun. 6(9),(1988) 1617-1622.
    """
    # validate input parameters
    if not isinstance(n, int) or n <= 0:
        raise ValueError('n must be a positive integer')
    if alpha > 1 or alpha <= 0 or beta > 1 or beta <= 0:
        raise ValueError('alpha and beta must be float values in (0,1]')
    if not isinstance(domain, tuple) or len(domain) != 4:
        raise ValueError('domain must be a tuple of 4 number')
    (xmin, ymin, xmax, ymax) = domain
    if xmin > xmax:
        raise ValueError('In domain, xmin cannot be greater than xmax')
    if  ymin > ymax:
        raise ValueError('In domain, ymin cannot be greater than ymax')
    if seed is not None:
        random.seed(seed)

    G = Topology(type='waxman_2', distance_unit=distance_unit)
    G.name = "waxman_2_topology(%s, %s, %s)" % (n, alpha, beta)
    G.add_nodes_from(range(n))


    for v in G.nodes():
        G.node[v]['latitude'] = (ymin + (ymax - ymin)) * random.random()
        G.node[v]['longitude'] = (xmin + (xmax - xmin)) * random.random()

    l = {}
    nodes = list(G.nodes())
    while nodes:
        u = nodes.pop()
        for v in nodes:
            x_u = G.node[u]['longitude']
            x_v = G.node[v]['longitude']
            y_u = G.node[u]['latitude']
            y_v = G.node[v]['latitude']
            l[(u, v)] = math.sqrt((x_u - x_v) ** 2 + (y_u - y_v) ** 2)
    L = max(l.values())
    for (u, v), d in l.items():
        if random.random() < alpha * math.exp(-d / (beta * L)):
            G.add_edge(u, v, length=d)

    return G


# This is the classical BA model, without rewiring and add
def barabasi_albert_topology(n, m, m0, seed=None):
    r"""
    Return a random topology using Barabasi-Albert preferential attachment
    model.

    A topology of n nodes is grown by attaching new nodes each with m links
    that are preferentially attached to existing nodes with high degree.

    More precisely, the Barabasi-Albert topology is built as follows. First, a
    line topology with m0 nodes is created. Then at each step, one node is
    added and connected to m existing nodes. These nodes are selected randomly
    with probability

    .. math::
            \Pi(i) = \frac{deg(i)}{sum_{v \in V} deg V}.

    Where i is the selected node and V is the set of nodes of the graph.

    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    m0 : int
        Number of nodes initially attached to the network
    seed : int, optional
        Seed for random number generator (default=None).

    Returns
    -------
    G : Topology

    Notes
    -----
    The initialization is a graph with with m nodes connected by :math:`m -1`
    edges.
    It does not use the Barabasi-Albert method provided by NetworkX because it
    does not allow to specify *m0* parameter.
    There are no disconnected subgraphs in the topology.

    References
    ----------
    .. [1] A. L. Barabasi and R. Albert "Emergence of scaling in
       random networks", Science 286, pp 509-512, 1999.
    """
    def calc_pi(G):
        """Calculate BA Pi function for all nodes of the graph"""
        degree = dict(G.degree())
        den = float(sum(degree.values()))
        return {node: degree[node] / den for node in G.nodes()}

    # input parameters
    if n < 1 or m < 1 or m0 < 1:
        raise ValueError('n, m and m0 must be positive integers')
    if m >= m0:
        raise ValueError('m must be <= m0')
    if n < m0:
        raise ValueError('n must be > m0')
    if seed is not None:
        random.seed(seed)
    # Step 1: Add m0 nodes. These nodes are interconnected together
    # because otherwise they will end up isolated at the end
    G = Topology(nx.path_graph(m0))
    G.name = "ba_topology(%d,%d,%d)" % (n, m, m0)
    G.graph['type'] = 'ba'

    # Step 2: Add one node and connect it with m links
    while G.number_of_nodes() < n:
        pi = calc_pi(G)
        u = G.number_of_nodes()
        G.add_node(u)
        new_links = 0
        while new_links < m:
            v = random_from_pdf(pi)
            if not G.has_edge(u, v):
                G.add_edge(u, v)
                new_links += 1
    return G


# This is the extended BA model, with rewiring and add
def extended_barabasi_albert_topology(n, m, m0, p, q, seed=None):
    r"""
    Return a random topology using the extended Barabasi-Albert preferential
    attachment model.

    Differently from the original Barabasi-Albert model, this model takes into
    account the presence of local events, such as the addition of new links or
    the rewiring of existing links.

    More precisely, the Barabasi-Albert topology is built as follows. First, a
    topology with *m0* isolated nodes is created. Then, at each step:
    with probability *p* add *m* new links between existing nodes, selected
    with probability:

    .. math::
        \Pi(i) = \frac{deg(i) + 1}{\sum_{v \in V} (deg(v) + 1)}

    with probability *q* rewire *m* links. Each link to be rewired is selected as
    follows: a node i is randomly selected and a link is randomly removed from
    it. The node i is then connected to a new node randomly selected with
    probability :math:`\Pi(i)`,
    with probability :math:`1-p-q` add a new node and attach it to m nodes of
    the existing topology selected with probability :math:`\Pi(i)`

    Repeat the previous step until the topology comprises n nodes in total.

    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    m0 : int
        Number of edges initially attached to the network
    p : float
        The probability that new links are added
    q : float
        The probability that existing links are rewired
    seed : int, optional
        Seed for random number generator (default=None).

    Returns
    -------
    G : Topology

    References
    ----------
    .. [1] A. L. Barabasi and R. Albert "Topology of evolving networks: local
       events and universality", Physical Review Letters 85(24), 2000.
    """
    def calc_pi(G):
        """Calculate extended-BA Pi function for all nodes of the graph"""
        degree = dict(G.degree())
        den = float(sum(degree.values()) + G.number_of_nodes())
        return {node: (degree[node] + 1) / den for node in G.nodes()}

    # input parameters
    if n < 1 or m < 1 or m0 < 1:
        raise ValueError('n, m and m0 must be a positive integer')
    if m >= m0:
        raise ValueError('m must be <= m0')
    if n < m0:
        raise ValueError('n must be > m0')
    if p > 1 or p < 0:
        raise ValueError('p must be included between 0 and 1')
    if q > 1 or q < 0:
        raise ValueError('q must be included between 0 and 1')
    if p + q > 1:
        raise ValueError('p + q must be <= 1')
    if seed is not None:
        random.seed(seed)
    G = Topology(type='extended_ba')
    G.name = "ext_ba_topology(%d, %d, %d, %f, %f)" % (n, m, m0, p, q)
    # Step 1: Add m0 isolated nodes
    G.add_nodes_from(range(m0))

    while G.number_of_nodes() < n:
        pi = calc_pi(G)
        r = random.random()

        if r <= p:
            # add m new links with probability p
            n_nodes = G.number_of_nodes()
            n_edges = G.number_of_edges()
            max_n_edges = (n_nodes * (n_nodes - 1)) / 2
            if n_edges + m > max_n_edges:  # cannot add m links
                continue  # rewire or add nodes
            new_links = 0
            while new_links < m:
                u = random_from_pdf(pi)
                v = random_from_pdf(pi)
                if u is not v and not G.has_edge(u, v):
                    G.add_edge(u, v)
                    new_links += 1

        elif r > p and r <= p + q:
            # rewire m links with probability q
            rewired_links = 0
            while rewired_links < m:
                i = random.choice(list(G.nodes()))  # pick up node randomly (uniform)
                if len(G.adj[i]) is 0:  # if i has no edges, I cannot rewire
                    break
                j = random.choice(list(G.adj[i].keys()))  # node to be disconnected
                k = random_from_pdf(pi)  # new node to be connected
                if i is not k and j is not k and not G.has_edge(i, k):
                    G.remove_edge(i, j)
                    G.add_edge(i, k)
                    rewired_links += 1
        else:
            # add a new node with probability 1 - p - q
            new_node = G.number_of_nodes()
            G.add_node(new_node)
            new_links = 0
            while new_links < m:
                existing_node = random_from_pdf(pi)
                if not G.has_edge(new_node, existing_node):
                    G.add_edge(new_node, existing_node)
                    new_links += 1
    return G


def glp_topology(n, m, m0, p, beta, seed=None):
    r"""
    Return a random topology using the Generalized Linear Preference (GLP)
    preferential attachment model.

    It differs from the extended Barabasi-Albert model in that there is link
    rewiring and a beta parameter is introduced to fine-tune preferential
    attachment.

    More precisely, the GLP topology is built as follows. First, a
    line topology with *m0* nodes is created. Then, at each step:
    with probability *p*, add *m* new links between existing nodes, selected
    with probability:

    .. math::
        \Pi(i) = \frac{deg(i) - \beta 1}{\sum_{v \in V} (deg(v) - \beta)}

    with probability :math:`1-p`, add a new node and attach it to m nodes of
    the existing topology selected with probability :math:`\Pi(i)`

    Repeat the previous step until the topology comprises n nodes in total.

    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    m0 : int
        Number of edges initially attached to the network
    p : float
        The probability that new links are added
    beta : float
        Parameter to fine-tune preferntial attachment: beta < 1
    seed : int, optional
        Seed for random number generator (default=None).

    Returns
    -------
    G : Topology

    References
    ----------
    .. [1] T. Bu and D. Towsey "On distinguishing between Internet power law
       topology generators", Proceeding od the 21st IEEE INFOCOM conference.
       IEEE, volume 2, pages 638-647, 2002.
    """
    def calc_pi(G, beta):
        """Calculate GLP Pi function for all nodes of the graph"""
        # validate input parameter
        if beta >= 1:
            raise ValueError('beta must be < 1')
        degree = dict(G.degree())
        den = float(sum(degree.values()) - (G.number_of_nodes() * beta))
        return {node: (degree[node] - beta) / den for node in G.nodes()}

    def add_m_links(G, pi):
        """Add m links between existing nodes to the graph"""
        n_nodes = G.number_of_nodes()
        n_edges = G.number_of_edges()
        max_n_edges = (n_nodes * (n_nodes - 1)) / 2
        if n_edges + m > max_n_edges:  # cannot add m links
            add_node(G, pi)  # add a new node instead
            # return in any case because before doing another operation
            # (add node or links) we need to recalculate pi
            return
        new_links = 0
        while new_links < m:
            u = random_from_pdf(pi)
            v = random_from_pdf(pi)
            if u != v and not G.has_edge(u, v):
                G.add_edge(u, v)
                new_links += 1

    def add_node(G, pi):
        """Add one node to the graph and connect it to m existing nodes"""
        new_node = G.number_of_nodes()
        G.add_node(new_node)
        new_links = 0
        while new_links < m:
            existing_node = random_from_pdf(pi)
            if not G.has_edge(new_node, existing_node):
                G.add_edge(new_node, existing_node)
                new_links += 1

    # validate input parameters
    if n < 1 or m < 1 or m0 < 1:
        raise ValueError('n, m and m0 must be a positive integers')
    if beta >= 1:
        raise ValueError('beta must be < 1')
    if m >= m0:
        raise ValueError('m must be <= m0')
    if p > 1 or p < 0:
        raise ValueError('p must be included between 0 and 1')
    if seed is not None:
        random.seed(seed)
    # step 1: create a graph of m0 nodes connected by n-1 edges
    G = Topology(nx.path_graph(m0))
    G.graph['type'] = 'glp'
    G.name = "glp_topology(%d, %d, %d, %f, %f)" % (n, m, m0, p, beta)
    # Add nodes and links now
    while G.number_of_nodes() < n:
        pi = calc_pi(G, beta)
        if random.random() < p:
            # add m new links with probability p
            add_m_links(G, pi)
        else:
            # add a new node with m new links with probability 1 - p
            add_node(G, pi)
    return G
