"""
Provides functions to deploy and configure protocol stacks and applications on
network nodes
"""

__all__ = ['add_stack',
           'get_stack',
           'remove_stack',
           'clear_stacks',
           'add_application',
           'get_application_names',
           'get_application_properties',
           'remove_application',
           'clear_applications',
           ]


def add_stack(topology, node, name, properties):
    """
    Set stack on a node
    
    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    name : str
        The name of the stack
    properties : dict
        The properties of the stack
    """
    if type(properties) != dict:
        raise ValueError('The properties parameter must be a dictionary')    
    topology.node[node]['stack'] = name, properties


def get_stack(topology, node):
    """
    Return the stack of a node, if any
    
    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    
    Returns
    -------
    stack : tuple (name, properties)
        A tuple of two values, where the first value is the name of the stack 
        and the second value is the dictionary of properties of the stack.
    """
    return None if 'stack' not in topology.node[node] \
                else topology.node[node]['stack']


def remove_stack(topology, node):
    """
    Remove stack from a node
    
    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    """
    if 'stack' in topology.node[node]:
        del topology.node[node]['stack']


def clear_stacks(topology):
    """
    Remove all stacks from all nodes of the topology
    
    Parameters
    ----------
    topology : Topology
    """
    for v in topology.nodes():
        if 'stack' in topology.node[v]:
            del topology.node[v]['stack']

def add_application(topology, node, name, properties):
    """
    Add an application to a node

    Parameters
    ----------
    topology : Topology
        The topology
    node : any hashable type
        The ID of the node
    name : str
        The name of the application
    properties : dict
        The properties of the application
    """
    if type(properties) != dict:
        raise ValueError('The properties parameter must be a dictionary')
    if 'application' not in topology.node[node]:
        topology.node[node]['application'] = {}
    topology.node[node]['application'][name] = properties


def get_application_names(topology, node):
    """
    Return a list of names of applications deployed on a node
    
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
    """
    Return a dictionary containing all the properties of an application
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
    """
    Remove an application from a node
    
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
    """
    Remove all applications from all nodes of the topology

    Parameters
    ----------
    topology : Topology
        The topology
    """
    for v in topology.nodes():
        if 'application' in topology.node[v]:
            del topology.node[v]['application']
