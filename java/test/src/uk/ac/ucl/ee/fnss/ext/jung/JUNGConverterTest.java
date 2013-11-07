package uk.ac.ucl.ee.fnss.ext.jung;

import static org.junit.Assert.assertNotNull;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import edu.uci.ics.jung.graph.Graph;

import uk.ac.ucl.ee.fnss.Edge;
import uk.ac.ucl.ee.fnss.Topology;

public class JUNGConverterTest {

	
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
		Graph<String, Edge> graph = JUNGConverter.getGraph(topology);
		assertNotNull(graph);
	}
	
}
