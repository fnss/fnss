package io.github.fnss.ext.jgrapht;

import io.github.fnss.Edge;
import io.github.fnss.Pair;
import io.github.fnss.Topology;

import org.jgrapht.Graph;
import org.jgrapht.WeightedGraph;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.jgrapht.graph.SimpleDirectedWeightedGraph;
import org.jgrapht.graph.SimpleGraph;
import org.jgrapht.graph.SimpleWeightedGraph;


/**
 * Utility class providing methods to convert FNSS <code>Topology</code>
 * objects to JGraphT graph objects.
 * 
 * @author Lorenzo Saino
 *
 */
public class JGraphTConverter {
	
	// prevent instantiation
	private JGraphTConverter() {}
	
	/**
	 * Convert FNSS Topology to JGraphT weighted graph.
	 * 
	 * The weights assigned to the edges of the returned graph are the link
	 * weights of the original FNSS topology. If the topology object does not
	 * have weights assigned, all nodes are assigned a weight equal to 1.
	 * 
	 * Because of the specific limitations of JGraphT, the edges of the returned
	 * graph must be instances of JGraphT <code>DefaultWeightedEdge</code>, and
	 * do not hold capacity, buffer sizes and delay information possibly present
	 * in the original FNSS Topology. The returned graph maintains however
	 * link weight information.
	 * 
	 * See examples for further information.
	 * 
	 * @param topology FNSS Topology object
	 * @return A JGraphT weighted graph
	 */
	public static WeightedGraph<String, DefaultWeightedEdge> getWeightedGraph(Topology topology) {
		WeightedGraph<String, DefaultWeightedEdge> graph = null;
		if (topology.isDirected()) {
			graph = new SimpleDirectedWeightedGraph<String, DefaultWeightedEdge>(DefaultWeightedEdge.class);
		} else {
			graph = new SimpleWeightedGraph<String, DefaultWeightedEdge>(DefaultWeightedEdge.class);
		}
		for(String node : topology.getAllNodes()) {
			graph.addVertex(node);
		}
		for(Pair<String, String> endpoints : topology.getAllEdges()) {
			float weight = topology.getEdge(endpoints).getWeight();
			DefaultWeightedEdge edge = new DefaultWeightedEdge();
			graph.addEdge(endpoints.getU(), endpoints.getV(), edge);
			graph.setEdgeWeight(edge, weight);
		}
		return graph;
	}

	/**
	 * Convert an FNSS Topology to a JGraphT graph.
	 * 
	 * @param topology FNSS Topology object
	 * @return A JGraphT graph
	 */
	public static Graph<String, Edge> getGraph(Topology topology) {
		Graph<String, Edge> graph = null;
		if (topology.isDirected()) {
			graph = new DefaultDirectedGraph<String, Edge>(Edge.class);
		} else {
			graph = new SimpleGraph<String, Edge>(Edge.class);
		}
		for(String node : topology.getAllNodes()) {
			graph.addVertex(node);
		}
		for(Pair<String, String> endpoints : topology.getAllEdges()) {
			Edge edge = topology.getEdge(endpoints);
			graph.addEdge(endpoints.getU(), endpoints.getV(), edge);
		}
		return graph;
	}

}
