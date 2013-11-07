package uk.ac.ucl.ee.fnss.ext.jgrapht;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;

import org.jgrapht.Graph;
import org.jgrapht.WeightedGraph;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import uk.ac.ucl.ee.fnss.Edge;
import uk.ac.ucl.ee.fnss.Topology;

public class JGraphTConverterTest {

	
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
	}

	@AfterClass
	public static void tearDownAfterClass() throws Exception {
	}

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}
	
	@Test
	public void testGetGraph() {
		Topology topology = new Topology();
		topology.addEdge("1", "2", new Edge());
		topology.addEdge("2", "3", new Edge());
		Graph<String, Edge> graph = JGraphTConverter.getGraph(topology);
		assertNotNull(graph);
		assertTrue(graph.containsEdge("1", "2"));
		assertTrue(graph.containsEdge("2", "3"));
		assertTrue(graph.containsEdge("2", "1"));
		assertTrue(graph.containsEdge("3", "2"));
	}

	@Test
	public void testGetGraphDirected() {
		Topology topology = new Topology(true);
		topology.addEdge("1", "2", new Edge());
		topology.addEdge("2", "3", new Edge());
		Graph<String, Edge> graph = JGraphTConverter.getGraph(topology);
		assertNotNull(graph);
		assertTrue(graph.containsEdge("1", "2"));
		assertTrue(graph.containsEdge("2", "3"));
		assertFalse(graph.containsEdge("2", "1"));
		assertFalse(graph.containsEdge("3", "2"));
	}
	
	@Test
	public void testGetWeightedGraph() {
		Topology topology = new Topology();
		topology.addEdge("1", "2", new Edge());
		topology.addEdge("2", "3", new Edge());
		WeightedGraph<String, DefaultWeightedEdge> graph = 
				JGraphTConverter.getWeightedGraph(topology);
		assertNotNull(graph);
		assertTrue(graph.containsEdge("1", "2"));
		assertTrue(graph.containsEdge("2", "3"));
		assertTrue(graph.containsEdge("2", "1"));
		assertTrue(graph.containsEdge("3", "2"));
	}

	@Test
	public void testGetWeightedGraphDirected() {
		Topology topology = new Topology(true);
		topology.addEdge("1", "2", new Edge());
		topology.addEdge("2", "3", new Edge());
		WeightedGraph<String, DefaultWeightedEdge> graph = 
				JGraphTConverter.getWeightedGraph(topology);
		assertNotNull(graph);
		assertTrue(graph.containsEdge("1", "2"));
		assertTrue(graph.containsEdge("2", "3"));
		assertFalse(graph.containsEdge("2", "1"));
		assertFalse(graph.containsEdge("3", "2"));
	}
}
