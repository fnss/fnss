************
Architecture
************

The Python core library is designed following a modular approach. 

All functionalities are splitted in three main packages:
 * **topologies**: contains all functions and classes for parsing or synthenically generating a network topology. 
   It also contains functions to read and write topology objects from/to an XML file. The conversion of such objects
   to XML files is needed to make topology available for hte Java and C++ API and the
   `ns-2 <http://www.isi.edu/nsnam/ns/>`_ and `ns-3 <http://www.nsnam.org/>`_ adapters.
 * **netconfig**: contains all functions for configuring a network topology. Such configuration include setting link
   capacities, delays and weights, set buffer sizes and deploy protocol stacks and applications on nodes.
 * **traffic**: contains all functions and classes for sythetically generating event schedules and traffic matrices.
 
In addition, the library also comprises a set of classes to model specific entities. These classes are:
 * **Topology**: a base undirected topology. Comprises methods for adding, editing and removing nodes and links. 
   This class inherits from `NetworkX <http://networkx.lanl.gov>`_ Graph class. 
   As a result, all graph algorithms and visualization tools provided by NetworkX can be used on Topology objects as well. 
 * **DirectedTopology**: a base directed topology. It shares most of the code of the Topology class but in this class links are directed.
   Similarly to the Topology class, this class inherits from `NetworkX <http://networkx.lanl.gov>`_ DiGraph class. 
 * **DatacenterTopology**: a datacenter topology.
   It inherits from the Topology class and comprises additional methods relevant only for datacenter topologies. 
 * **TrafficMatrix**: a traffic matrix, capturing the average traffic on a network at a specific point in time.
 * **TrafficMatrixSequence**: a sequence of traffic matrices, capturing the evolution of traffic on a network over a period of time. 
 * **EventSchedule**: a schedule of events to be simulated.
 
In order to make the simulation setup information created with FNSS core library (topology, traffic, events) available to the desired target simulator, FNSS provides the capability to export such information to XML files. These XML files can then be read by the Java or C++ APIs or by the ns-2 and ns-3 adapters. 
More specifically, the following objects can be saved to XML files:
 * **Topology**, **DirectedTopology**, **DatacenterTopology** and any potential subclasses can be writted to XML files with the function ``write_topology``.
 * **TrafficMatrix**, **TrafficMatrixSequence** and any potential subclasses can be writted to XML files with the function ``write_traffic_matrix``.
 * **EventSchedule** and any potential subclasses can be writted to XML files with the function ``write_event_schedule``.
  
