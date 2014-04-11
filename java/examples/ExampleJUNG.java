import io.github.fnss.Edge;
import io.github.fnss.Topology;
import io.github.fnss.ext.jung.JUNGConverter;

import java.util.List;

import edu.uci.ics.jung.algorithms.shortestpath.DijkstraShortestPath;
import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.util.Pair;

/**
 * This example shows how to convert an FNSS topology object into a JUNG
 * graph and calculate shortest paths using JUNG's implementation of the
 * Dijkstra's algorithm
 * 
 * @author Lorenzo Saino
 *
 */
public class ExampleJUNG {
	
	public static void main(String[] args) {
		// create FNSS topology
		Topology topology = new Topology();
		topology.addEdge("1", "2", new Edge());
		topology.addEdge("2", "3", new Edge());
		
		// convert to JGraphT
		Graph<String, Edge> graph = JUNGConverter.getGraph(topology);
		
		// Find shortest paths
		String source = "3";
		String destination = "1";
		DijkstraShortestPath<String, Edge> shortestPath = 
				new DijkstraShortestPath<String, Edge>(graph);
		List<Edge> path = shortestPath.getPath(source, destination);

		// Print results
		System.out.println("Shortest path from " + source + " to " + destination + ":");
		for (Edge e : path) {
			Pair<String> endpoints = graph.getEndpoints(e);
			System.out.println(endpoints.getFirst() + " -> " + endpoints.getSecond());
		}
	}
}
