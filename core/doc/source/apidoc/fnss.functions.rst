Functions
=========

:mod:`netconfig` package
------------------------

:mod:`buffers` module
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.netconfig.buffers
.. autosummary::
   :toctree: generated/

    clear_buffer_sizes
    get_buffer_sizes
    set_buffer_sizes_bw_delay_prod
    set_buffer_sizes_constant
    set_buffer_sizes_link_bandwidth

:mod:`capacities` module
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.netconfig.capacities
.. autosummary::
   :toctree: generated/

    clear_capacities
    get_capacities
    set_capacities_betweenness_gravity
    set_capacities_communicability_gravity
    set_capacities_constant
    set_capacities_degree_gravity
    set_capacities_edge_betweenness
    set_capacities_edge_communicability
    set_capacities_eigenvector_gravity
    set_capacities_pagerank_gravity
    set_capacities_random
    set_capacities_random_power_law
    set_capacities_random_uniform
    set_capacities_random_zipf
    set_capacities_random_zipf_mandelbrot

:mod:`delays` module
^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.netconfig.delays
.. autosummary::
   :toctree: generated/

    clear_delays
    get_delays
    set_delays_constant
    set_delays_geo_distance

:mod:`nodeconfig` module
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.netconfig.nodeconfig
.. autosummary::
   :toctree: generated/

    add_application
    add_stack
    clear_applications
    clear_stacks
    get_application_names
    get_application_properties
    get_stack
    remove_application
    remove_stack

:mod:`weights` module
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.netconfig.weights
.. autosummary::
   :toctree: generated/

    clear_weights
    get_weights
    set_weights_constant
    set_weights_delays
    set_weights_inverse_capacity

:mod:`traffic` package
----------------------

:mod:`eventscheduling` module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.traffic.eventscheduling
.. autosummary::
   :toctree: generated/

    deterministic_process_event_schedule
    poisson_process_event_schedule
    read_event_schedule
    write_event_schedule

:mod:`trafficmatrices` module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.traffic.trafficmatrices
.. autosummary::
   :toctree: generated/

    link_loads
    read_traffic_matrix
    sin_cyclostationary_traffic_matrix
    static_traffic_matrix
    stationary_traffic_matrix
    validate_traffic_matrix
    write_traffic_matrix

:mod:`topologies` package
-------------------------

:mod:`datacenter` module
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.topologies.datacenter
.. autosummary::
   :toctree: generated/

    bcube_topology
    fat_tree_topology
    three_tier_topology
    two_tier_topology

:mod:`parsers` module
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.topologies.parsers
.. autosummary::
   :toctree: generated/

    parse_abilene
    parse_ashiip
    parse_brite
    parse_caida_as_relationships
    parse_inet
    parse_rocketfuel_isp_map
    parse_topology_zoo

:mod:`randmodels` module
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.topologies.randmodels
.. autosummary::
   :toctree: generated/

    barabasi_albert_topology
    erdos_renyi_topology
    extended_barabasi_albert_topology
    glp_topology
    waxman_1_topology
    waxman_2_topology

:mod:`simplemodels` module
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.topologies.simplemodels
.. autosummary::
   :toctree: generated/

    chord_topology
    dumbbell_topology
    full_mesh_topology
    k_ary_tree_topology
    line_topology
    ring_topology
    star_topology

:mod:`topology` module
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.topologies.topology
.. autosummary::
   :toctree: generated/

    fan_in_out_capacities
    od_pairs_from_topology
    rename_edge_attribute
    rename_node_attribute
    read_topology
    write_topology

:mod:`adapters` package
-------------------------

:mod:`autonetkit` module
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fnss.adapters.autonetkit
.. autosummary::
   :toctree: generated/

    from_autonetkit
    to_autonetkit

:mod:`mn` module
^^^^^^^^^^^^^^^^

.. automodule:: fnss.adapters.mn
.. autosummary::
   :toctree: generated/

    from_mininet
    to_mininet

:mod:`ns2` module
^^^^^^^^^^^^^^^^^

.. automodule:: fnss.adapters.ns2
.. autosummary::
   :toctree: generated/

    to_ns2
    validate_ns2_stacks