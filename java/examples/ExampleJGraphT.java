import io.github.fnss.Edge;
import io.github.fnss.Topology;
import io.github.fnss.ext.jgrapht.JGraphTConverter;

import java.util.List;

import org.jgrapht.Graph;
import org.jgrapht.WeightedGraph;
import org.jgrapht.alg.DijkstraShortestPath;
import org.jgrapht.graph.DefaultWeightedEdge;


/**
 * This example shows how to convert an FNSS topology object into a JGraphT
 * graph and calculate shortest paths using JGraphT's implementation of the
 * Dijkstra's algorithm 
 * 
 * @author Lorenzo Saino
 *
 */
public class ExampleJGraphT {
	
	
	/**
	 * Shows how to create an FNSS Topology with weighted edges, convert it to
	 * a JGraphT WeightedGraph and then compute shortest paths
	 */
	public static void exampleWeightedGraph() {
		
		// create unidrected topology
		Topology topology = new Topology();
		
		// Create edge with high weight and edge with low weight
		Edge edgeHighWeight = new Edge();
		edgeHighWeight.setWeight(1000);
		
		Edge edgeLowWeight = new Edge();
		edgeLowWeight.setWeight(1);
		
		// Assign edges to topology
		topology.addEdge("1", "4", edgeHighWeight);
		topology.addEdge("2", "3", edgeLowWeight);
		topology.addEdge("1", "2", edgeLowWeight);
		topology.addEdge("4", "3", edgeLowWeight);
		
		// convert to JGraphT
		WeightedGraph<String, DefaultWeightedEdge> graph = 
				JGraphTConverter.getWeightedGraph(topology);
		
		// Find shortest paths
		String source = "1";
		String destination = "3";
		List<DefaultWeightedEdge> sp = 
				DijkstraShortestPath.findPathBetween(graph, source, destination);
		
		// Print results
		System.out.println("Shortest path from " + source + " to " + destination + ":");
		for (DefaultWeightedEdge e : sp) {
			System.out.println(graph.getEdgeSource(e) + " -> " + graph.getEdgeTarget(e));
		}
	}
	
	/**
	 * Shows how to create an FNSS Topology, convert it to a JGraphT Graph and
	 * then compute shortest paths
	 */
	public static void exampleGraph() {
		// create a simple FNSS topology
		Topology topology = new Topology();
		topology.addEdge("1", "2", new Edge());
		topology.addEdge("2", "3", new Edge());
		
		// convert to JGraphT
		Graph<String, Edge> graph = JGraphTConverter.getGraph(topology);
		
		// Find shortest paths
		String source = "3";
		String destination = "1";
		List<Edge> sp = DijkstraShortestPath.findPathBetween(graph, source, destination);
		
		// Print results
		System.out.println("Shortest path from " + source + " to " + destination + ":");
		for (Edge e : sp) {
			System.out.println(graph.getEdgeSource(e) + " -> " + graph.getEdgeTarget(e));
		}
	}
	
	public static void main(String[] args) {
		exampleGraph();
		exampleWeightedGraph();
	}
}
