"""Functions to deploy and configure protocol stacks and applications
on network nodes
"""

__all__ = [
    'add_stack',
    'get_stack',
    'remove_stack',
    'clear_stacks',
    'add_application',
    'get_application_names',
    'get_application_properties',
    'remove_application',
    'clear_applications',
           ]


def add_stack(topology, node, name, properties=None, **kwargs):
    """Set stack on a node.

    If the node already has a stack, it is overwritten

    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    name : str
        The name of the stack
    properties : dict, optional
        The properties of the stack
    **attr : keyworded attributes
        Further properties of the application
    """
    if properties is None:
        properties = {}
    elif not isinstance(properties, dict):
        raise TypeError('The properties parameter must be a dictionary')
    properties.update(kwargs)
    topology.node[node]['stack'] = name, properties


def get_stack(topology, node, data=True):
    """Return the stack of a node, if any

    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    data : bool, optional
        If true, returns a tuple of the stack name and its attributes,
        otherwise just the stack name

    Returns
    -------
    stack : tuple (name, properties) or name only
        If data = True, a tuple of two values, where the first value is the
        name of the stack and the second value is the dictionary of its
        properties.
        If data = False returns only the stack name
        If no stack is deployed, return None
    """
    if 'stack' not in topology.node[node]:
        return None
    name, props = topology.node[node]['stack']
    return (name, props) if data else name


def remove_stack(topology, node):
    """Remove stack from a node

    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    """
    topology.node[node].pop('stack', None)


def clear_stacks(topology):
    """Remove all stacks from all nodes of the topology

    Parameters
    ----------
    topology : Topology
    """
    for v in topology.nodes():
        topology.node[v].pop('stack', None)

def add_application(topology, node, name, properties=None, **attr):
    """Add an application to a node

    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    name : str
        The name of the application
    attr_dict : dict, optional
        Attributes of the application
    **attr : keyworded attributes
        Attributes of the application
    """
    if properties is None:
        properties = {}
    elif not isinstance(properties, dict):
        raise TypeError('The attr_dict parameter must be a dictionary')
    properties.update(attr)
    if 'application' not in topology.node[node]:
        topology.node[node]['application'] = {}
    topology.node[node]['application'][name] = properties


def get_application_names(topology, node):
    """Return a list of names of applications deployed on a node

    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node

    Returns
    -------
    application_names : list
        A list of application names
    """
    return [] if 'application' not in topology.node[node] \
              else list(topology.node[node]['application'].keys())


def get_application_properties(topology, node, name):
    """Return a dictionary containing all the properties of an application
    deployed on a node

    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    name : str
        The name of the application

    Returns
    -------
    applications : dict
        A dictionary containing the properties of the application
    """
    if 'application' not in topology.node[node]:
        raise ValueError('There is no such application deployed on the node')
    return topology.node[node]['application'][name]


def remove_application(topology, node, name=None):
    """Remove an application from a node

    Parameters
    ----------
    topology : Topology
        The topology object
    node : any hashable type
        The ID of the node from which the application is to be removed
    name : optional
        The name of the application to remove. If not given, all the
        applications of the node are removed
    """
    if 'application' in topology.node[node]:
        if name is None:
            del topology.node[node]['application']
        elif name in topology.node[node]['application']:
            del topology.node[node]['application'][name]


def clear_applications(topology):
    """Remove all applications from all nodes of the topology

    Parameters
    ----------
    topology : Topology
        The topology
    """
    for v in topology.nodes():
        topology.node[v].pop('application', None)
