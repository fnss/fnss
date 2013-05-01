package uk.ac.ucl.ee.fnss;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Represent a network topology
 * 
 * @author Lorenzo Saino
 */
public class Topology extends PropertyContainer implements Cloneable {

	private Map<String, Node> nodes = new Hashtable<String, Node>();

	private Map<String, Map<String, Edge>> adjacencyMatrix = 
			new Hashtable<String, Map<String, Edge>>();
	
	private boolean isDirected = false;
	
	private String capacityUnit = null;
	private String delayUnit = null;
	private String distanceUnit = null;
	private String bufferUnit = null;

	/**
	 * Constructor
	 */
	public Topology() { }

	/**
	 * Constructor
	 * 
	 * @param directed <code>true</code> if edges are directed,
	 * <code>false</code> otherwise
	 */
	public Topology(boolean directed) {
		this.isDirected = directed;
	}

	/**
	 * Return the type of edges
	 * 
	 * @return <code>true</code> if edges are directed, <code>false</code>
	 */
	public boolean isDirected() {
		return isDirected;
	}

	/**
	 * Makes this topology directed. If it is already directed,
	 * nothing happens.
	 */
	public void makeDirected() {
		this.isDirected = true;
	}

	/**
	 * Return the unit of link capacity
	 * 
	 * @return the capacity unit
	 */
	public String getCapacityUnit() {
		return capacityUnit;
	}

	/**
	 * Set the unit of link capacity
	 * 
	 * @param capacityUnit the capacity unit to set
	 */
	public void setCapacityUnit(String capacityUnit) {
		if (!Units.isValidCapacityUnit(capacityUnit)) {
			throw new IllegalArgumentException(
					"The value of the capacityUnit parameter is not valid");
		}
		this.capacityUnit = capacityUnit;
	}

	/**
	 * Return the unit of link delay
	 * 
	 * @return the delay unit
	 */
	public String getDelayUnit() {
		return delayUnit;
	}

	/**
	 * Set the unit of link delay
	 * 
	 * @param delayUnit the delay unit to set
	 */
	public void setDelayUnit(String delayUnit) {
		if (!Units.isValidDelayUnit(delayUnit)) {
			throw new IllegalArgumentException(
					"The value of the delayUnit parameter is not valid");
		}
		this.delayUnit = delayUnit;
	}

	/**
	 * Return the unit of geographical distance (used for link lengths)
	 * 
	 * @return the distance unit
	 */
	public String getDistanceUnit() {
		if (!Units.isValidDistanceUnit(distanceUnit)) {
			throw new IllegalArgumentException(
					"The value of the distanceUnit parameter is not valid");
		}
		return distanceUnit;
	}

	/**
	 * Set the unit of geographical distance (used for nodes coordinates and
	 * link lengths)
	 * 
	 * @param distanceUnit the distance unit to set
	 */
	public void setDistanceUnit(String distanceUnit) {
		this.distanceUnit = distanceUnit;
	}

	/**
	 * Return the unit of buffer size
	 * 
	 * @return the buffer unit
	 */
	public String getBufferUnit() {
		return bufferUnit;
	}

	/**
	 * Set the unit of buffer size
	 * 
	 * @param bufferUnit the buffer unit to set
	 */
	public void setBufferUnit(String bufferUnit) {
		if (!Units.isValidBufferUnit(bufferUnit)) {
			throw new IllegalArgumentException(
					"The value of the bufferUnit parameter is not valid");
		}
		this.bufferUnit = bufferUnit;
	}

	/**
	 * Add a node to the topology
	 * 
	 * @param v The ID of the node
	 * @param node The Node object
	 */
	public void addNode(String v, Node node) {
		nodes.put(v, node.clone());
	}

	/**
	 * Remove a node to the topology.
	 * 
	 * @param v The ID of the node to remove
	 * @return The <code>Node</code> object removed if it was present in the
	 * topology. Otherwise, <code>null</code> is returned
	 */
	public Node removeNode(String v) {
		return nodes.remove(v);
	}

	/**
	 * Return a specific node of the topology
	 * 
	 * @param v The ID of the node
	 * @return The selected node, if present. Otherwise <code>null</code> 
	 * is returned
	 */
	public Node getNode(String v) {
		return nodes.get(v);
	}

	/**
	 * Return a set containing all the node IDs. To get the Node object of a 
	 * specific node use <code>getNode(String v)</code>
	 * 
	 * @return a set with all node IDs of the topology
	 * 
	 * @see #getNode(String)
	 */
	public Set<String> getAllNodes() {
		return nodes.keySet();
	}

	/**
	 * Return the number of nodes in the topology
	 * 
	 * @return the number of nodes
	 */
	public int numberOfNodes() {
		return nodes.size();
	}
	
	/**
	 * Add an edge to the topology. If the nodes connected by the edge are not
	 * present, they are created.
	 * 
	 * @param u The start node
	 * @param v The end node
	 */
	public void addEdge(String u, String v) {
		addEdge(u, v, new Edge());
	}
	
	/**
	 * Add an edge to the topology. If the nodes connected by the edge are not
	 * present, they are created.
	 * 
	 * @param u The start node
	 * @param v The end node
	 * @param edge The edge object
	 */
	public void addEdge(String u, String v, Edge edge) {
		edge = edge.clone();
		if (!nodes.containsKey(u)) {
			nodes.put(u, new Node());
		}
		if (!nodes.containsKey(v)) {
			nodes.put(v, new Node());
		}
		if(!adjacencyMatrix.containsKey(u)){
			adjacencyMatrix.put(u, new HashMap<String, Edge>());
		}
		adjacencyMatrix.get(u).put(v, edge);
		// if the graph is undirected, we add an edge also in the other
		// direction but the Edge object to which they point is the same
		if (!isDirected) {
			if(!adjacencyMatrix.containsKey(v)){
				adjacencyMatrix.put(v, new HashMap<String, Edge>());
			}
			adjacencyMatrix.get(v).put(u, edge);
		}
	}

	/**
	 * Remove an edge from the topology
	 * 
	 * @param u The start node
	 * @param v The end node
	 * @return The removed egde, if it was present. Otherwise, 
	 * <code>null</code> is returned.
	 */
	public Edge removeEdge(String u, String v) {
		if (!isDirected) {
			adjacencyMatrix.get(v).remove(u);
		}
		return adjacencyMatrix.get(u).remove(v);
	}
	
	/**
	 * Return a specific edge in the topology
	 * 
	 * @param u The edge start node
	 * @param v The edge end node
	 * @return The selected edge, if present. Otherwise <code>null</code> is
	 * returned
	 */
	public Edge getEdge(String u, String v) {
		if (!adjacencyMatrix.containsKey(u)) {
			return null;
		}
		return adjacencyMatrix.get(u).get(v);
	}

	/**
	 * Return a specific edge in the topology
	 * 
	 * @param endpoints a pair containing edge endpoints
	 * @return The selected edge, if present. Otherwise <code>null</code> is 
	 * returned
	 */
	public Edge getEdge(Pair<String, String> endpoints) {
		return getEdge(endpoints.getU(), endpoints.getV());
	}

	/**
	 * Return a set containing all the edge endpoints pair. To get the Edge 
	 * object of a specific edge use <code>getEdge(String v, String u)</code>
	 * 
	 * @return a set with all edge endpoint pairs of the topology
	 * 
	 * @see #getEdge(String, String)
	 */
	public Set<Pair<String, String>> getAllEdges() {
		Set<Pair<String, String>> edges = new HashSet<Pair<String, String>>();
		List<String> seen = new ArrayList<String>();
		for (String u : adjacencyMatrix.keySet()) {
			seen.add(u);
			for (String v : adjacencyMatrix.get(u).keySet()) {
				if(!seen.contains(v) || isDirected) {
					edges.add(new Pair<String, String>(u, v));
				}
			}
		}
		return edges;
	}

	/**
	 * Return the number of edges in the topology
	 *
	 * @return the number of edges
	 */
	public int numberOfEdges() {
		int numberOfEdges = 0;
		for (Map<String, Edge> row : adjacencyMatrix.values()) {
			numberOfEdges += row.size();
		}
		return isDirected ? numberOfEdges : numberOfEdges/2;
	}

	/**
	 * Return a copy of this object
	 * 
	 * @return A copy of this object
	 */
	@Override
	public Topology clone() {
		Topology clone = (Topology) super.clone();
		
		Map<String, Node> clonedNodes = new Hashtable<String, Node>();
		for (String key : nodes.keySet()) {
			clonedNodes.put(key, nodes.get(key).clone());
		}
		nodes = clonedNodes;
		
		Map<String, Map<String, Edge>> clonedAdjacencyMatrix = 
				new Hashtable<String, Map<String, Edge>>();
		List<String> seen = new ArrayList<String>();
		for (String u : adjacencyMatrix.keySet()) {
			clonedAdjacencyMatrix.put(u, new HashMap<String, Edge>());
			seen.add(u);
			for (String v : adjacencyMatrix.get(u).keySet()) {
				if (seen.contains(v) && !isDirected) {
					clonedAdjacencyMatrix.get(u).put(v, clonedAdjacencyMatrix.get(v).get(u));
				} else {
					clonedAdjacencyMatrix.get(u).put(v, adjacencyMatrix.get(u).get(v).clone());
				}
			}
		}
		adjacencyMatrix = clonedAdjacencyMatrix;
		return clone;
	}

}
