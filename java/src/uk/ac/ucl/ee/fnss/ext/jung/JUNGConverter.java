package uk.ac.ucl.ee.fnss.ext.jung;

import uk.ac.ucl.ee.fnss.Edge;
import uk.ac.ucl.ee.fnss.Pair;
import uk.ac.ucl.ee.fnss.Topology;
import edu.uci.ics.jung.graph.DirectedSparseGraph;
import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.UndirectedSparseGraph;
import edu.uci.ics.jung.graph.util.EdgeType;

/**
 * Utility class providing methods to convert an FNSS <code>Topology</code>
 * object to a JUNG <code>Graph</code> object.
 * 
 * @author Lorenzo Saino
 *
 */
public class JUNGConverter {
	
	// prevent instantiation
	private JUNGConverter() {}
	
	/**
	 * Convert FNSS topology to JUNG graph.
	 * 
	 * @param topology FNSS Topology object
	 * @return A JUNG graph
	 */
	public static Graph<String, Edge> getGraph(Topology topology) {
		Graph<String, Edge> graph = null;
		EdgeType edgeType = null;
		if (topology.isDirected()) {
			graph = new DirectedSparseGraph<String, Edge>();
			edgeType = EdgeType.DIRECTED;
		} else {
			graph = new UndirectedSparseGraph<String, Edge>();
			edgeType = EdgeType.UNDIRECTED;
		}
		for(String node : topology.getAllNodes()) {
			graph.addVertex(node);
		}
		for(Pair<String, String> edge : topology.getAllEdges()) {
			graph.addEdge(topology.getEdge(edge), edge.getU(), edge.getV(), edgeType);
		}
		return graph;
	}
	
}
