"""Measurement units used by FNSS"""

__all__ = [
    'capacity_units',
    'time_units',
    'distance_units',
    'convert_capacity_value',
    'convert_time_value'
          ]


# Average Earth radius, in Km
EARTH_RADIUS = 6371

distance_units = {'m': 0.001, 'km': 1, 'Km': 1}

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


def convert_capacity_value(value, old_unit, new_unit):
    """Convert a capacity value from a unit to another one.

    Parameters
    ----------
    value : float
        Value of a measure to convert
    old_unit : str
        Unit from which the conversion is made
    new_unit : str
        Unit to which the conversion is made

    Returns
    -------
    converted_value : float
        Capacity value in the new unit
    """
    return value * capacity_units[old_unit] / capacity_units[new_unit]

def convert_time_value(value, old_unit, new_unit):
    """Convert a time/delay value from a unit to another one.

    Parameters
    ----------
    value : float
        Value of a measure to convert
    old_unit : str
        Unit from which the conversion is made
    new_unit : str
        Unit to which the conversion is made

    Returns
    -------
    converted_value : float
        Time/delay value in the new unit
    """
    return value * time_units[old_unit] / time_units[new_unit]
