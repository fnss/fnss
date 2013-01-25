"""
Provide basic utility functions
"""
from random import random
from ast import literal_eval

__all__ = ['capacity_units',
           'time_units',
          ]


# http://en.wikipedia.org/wiki/Data_rate_units
capacity_units = {'Tbps': 10**12,        'Gbps': 10**9,      'Mbps': 10**6,      
                  'Kbps': 1000,          'kbps': 1000,       'bps': 1,
                  'Tbit/s': 10**12,      'Gbit/s': 10**9,    'Mbit/s': 10**6,    
                  'Kbit/s': 1000,        'kbit/s': 1000,     'bit/s': 1,
                  'Tb': 10**12,          'Gb': 10**9,        'Mb': 10**6,        
                  'Kb': 1000,            'kb': 1000,         'b': 1,
                  'TBps': 8*(10**12),    'GBps': 8*(10**9),  'MBps': 8*(10**6),  
                  'KBps': 8000,          'kBps': 8000,       'Bps': 8,
                  'TB/s': 8*(10**12),    'GB/s': 8*(10**9),  'MB/s': 8*(10**6),  
                  'KB/s': 8000,          'kB/s': 8000,       'B/s': 8,
                  'TB': 8*(10**12),      'GB': 8*(10**9),    'MB': 8*(10**6),    
                  'KB': 8000,            'kB': 8000,         'B': 8
                  }


time_units = {'minutes': 60*10**3,      'minute': 60*10**3,
              'min': 60*10**3,          'm': 60*10**3,
              'seconds': 10**3,         'second': 10**3,
              'sec': 10**3,             's': 10**3,
              'milliseconds': 1,        'millisecond': 1,
              'millisec': 1,            'ms': 1,
              'microseconds': 0.001,    'microsecond': 0.001,
              'microsec': 0.001,        'us': 0.001,
              'nanoseconds': 0.000001,  'nanosecond': 0.000001,
              'nanosec': 0.000001,      'ns': 0.000001
              }


def split_list(l, size):
    """
    Splits a list into evenly sized chunks
    
    Parameters
    ----------
    l : list
        The list to split
    size : n
        The size of each chunk
        
    Returns
    -------
    A list of sub-lists
    """
    return [l[i: i + size] for i in range(0, len(l), size)]


def random_from_pdf(pdf):
    """
    Return a random value according to a given probability density function.
    
    Parameters
    ----------
    pdf : dict
        Dictionary mapping values of the random variable and probability of
        occurrence. The sum of all dictionary values must be 1.
        
    Example
    -------
    >>> pdf = {100: 0.5, 200: 0.5}
    >>> random_from_pdf(pdf)
    100 # random
    """
    # validate input parameters
    if(type(pdf) != dict):
        raise ValueError('The parameter pdf must be a dictionary')
    if abs(sum(pdf.values()) - 1) > 0.0001:
        raise ValueError('The sum of all probabilities must be equal to 1')
    r = random()
    w = 0.0
    for key, value in pdf.items():
        w += value
        if r < w:
            return key


def _xml_cast_type(type_attrib, val):
    """
    Cast a value read to an XML to an appropriate Python type
    
    Parameters
    ----------
    type_attrib : str
        The type of the value as specified in the XML file
    val : str
        The value to cast
        
    Returns
    -------
    cast_val : any type
        The val argument cast to a given type 
    """
    if type_attrib == 'int':
        return int(val)
    elif type_attrib == 'float':
        return float(val)
    elif type_attrib == 'boolean':
        return bool(val)
    elif type_attrib in ['tuple', 'list', 'dict']:
        return literal_eval(val)
    else:
        return val


def _xml_type(val):
    """
    Return a type string for writing to an XML file.
    
    Parameters
    ----------
    val : any type
        The value
    
    Returns
    -------
    type : str
        The type of the value to insert in the XML file
    """
    if type(val) is str:
        return 'string'
    elif type(val) is int:
        return 'int'
    elif type(val) is bool:
        return 'boolean'
    elif type(val) is float:
        return 'float'
    elif type(val) is tuple:
        return 'tuple'
    elif type(val) is dict:
        return 'dict'
    elif type(val) is list:
        return 'list'
    else:
        return 'string'


def _xml_indent(elem, level=0):
    """
    Indent the elements of the XML tree
    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _xml_indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
