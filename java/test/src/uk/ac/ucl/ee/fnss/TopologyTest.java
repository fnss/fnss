package uk.ac.ucl.ee.fnss;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

public class TopologyTest {

	
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
	public void testConstructor() {
		Topology dirTopology = new Topology(true);
		Topology undirTopology = new Topology(false);
		Topology defaultTopology = new Topology(); // undirected
		assertTrue(dirTopology.isDirected());
		assertFalse(undirTopology.isDirected());
		assertFalse(defaultTopology.isDirected());
	}
	
	@Test
	public void testProperties() {
		Topology topology = new Topology();
		topology.setProperty("name1", "value1");
		topology.setProperty("name2", "value2");
		assertEquals("value1", topology.getProperty("name1"));
		assertEquals(2, topology.getAllProperties().size());
		assertTrue(topology.getAllProperties().contains("name1"));
		assertTrue(topology.getAllProperties().contains("name2"));
		topology.removeProperty("name1");
		assertFalse(topology.getAllProperties().contains("name1"));
		assertNull(topology.getProperty("namenull"));
	}	

	@Test
	public void testAddEdgeUndirected() {
		Edge edge = new Edge();
		edge.setCapacity(100);
		Topology topology = new Topology(false);
		topology.addEdge("a", "b", edge);
		assertNotNull(topology.getEdge("a", "b"));
		assertNotNull(topology.getEdge("b", "a"));
		assertNotNull(topology.getNode("a"));
		assertNotNull(topology.getNode("b"));
		topology.getEdge("a", "b").setCapacity(200);
		assertEquals(200, topology.getEdge("b", "a").getCapacity(), 0.1);
		assertEquals(100, edge.getCapacity(), 0.1);
	}
	
	@Test
	public void testAddEdgeDirected() {
		Topology topology = new Topology(true);
		topology.addEdge("a", "b", new Edge());
		assertNotNull(topology.getEdge("a", "b"));
		assertNull(topology.getEdge("b", "a"));
		assertNotNull(topology.getNode("a"));
		assertNotNull(topology.getNode("b"));
	}
	
	@Test
	public void testRemoveEdgeDirected() {
		Topology topology = new Topology(true);
		topology.addEdge("a", "b", new Edge());
		topology.addEdge("b", "a", new Edge());
		topology.removeEdge("a", "b");
		assertNotNull(topology.getEdge("b", "a"));
		assertNull(topology.getEdge("a", "b"));
		assertNotNull(topology.getNode("a"));
		assertNotNull(topology.getNode("b"));
		topology.removeEdge("b", "a");
		assertNull(topology.getEdge("b", "a"));
		assertNotNull(topology.getNode("a"));
		assertNotNull(topology.getNode("b"));
	}
	
	@Test
	public void testRemoveEdgeUndirected() {
		Topology topology = new Topology(false);
		topology.addEdge("a", "b", new Edge());
		topology.addEdge("b", "a", new Edge());
		topology.removeEdge("a", "b");
		assertNull(topology.getEdge("b", "a"));
		assertNull(topology.getEdge("a", "b"));
		assertNotNull(topology.getNode("a"));
		assertNotNull(topology.getNode("b"));
	}
	
	@Test
	public void testEdgeCopy() {
		Edge edge1 = new Edge();
		edge1.setCapacity(100);
		edge1.setProperty("name", "value1");
		Edge edge2 = edge1.clone();
		edge2.setCapacity(200);
		edge2.setProperty("name", "value2");
		assertEquals(100, edge1.getCapacity(), 0.1);
		assertEquals("value1", edge1.getProperty("name"));
	}
	
	@Test
	public void testProtocolStackCopy() {
		ProtocolStack stack1 = new ProtocolStack("name");
		stack1.setProperty("name", "value1");
		ProtocolStack stack2 = stack1.clone();
		stack2.setProperty("name", "value2");
		assertEquals("value1", stack1.getProperty("name"));
	}
	
	@Test
	public void testApplicationCopy() {
		Application app1 = new Application("name1");
		app1.setProperty("name", "value1");
		Application app2 = app1.clone();
		app2.setProperty("name", "value2");
		app2.setName("name2");
		assertEquals("value1", app1.getProperty("name"));
		assertEquals("name1", app1.getName());
		
	}
	
	@Test
	public void testNodeCopy() {
		Node node1 = new Node();
		node1.setProperty("name", "value1");
		Node node2 = node1.clone();
		node2.setProperty("name", "value2");
		assertEquals("value1", node1.getProperty("name"));
	}

	@Test
	public void testaddNode() {
		Node node = new Node();
		node.setProperty("name", "value1");
		Topology topology = new Topology();
		topology.addNode("node1", node);
		assertNotNull(topology.getNode("node1"));
		assertNull(topology.getNode("node2"));
		node.setProperty("name", "value2");
		assertEquals("value1", topology.getNode("node1").getProperty("name"));
	}
	
	
	@Test
	public void testNumberOfNodes() {
		Topology topology = new Topology(false);
		topology.addEdge("a", "b", new Edge());
		topology.addEdge("b", "c", new Edge());
		assertEquals(3, topology.numberOfNodes());
	}
	
	@Test
	public void testOverwriteEdgeUndirected() {
		Topology topology = new Topology(false);
		Edge edge1 = new Edge();
		edge1.setProperty("name", "value1");
		Edge edge2 = new Edge();
		edge2.setProperty("name", "value2");
		topology.addEdge("a", "b", edge1);
		topology.addEdge("b", "a", edge2);
		assertEquals("value2", topology.getEdge("a","b").getProperty("name"));
	}
	
	@Test
	public void testNumberOfEdgesUndirected() {
		Topology topology = new Topology(false);
		topology.addEdge("a", "b", new Edge());
		topology.addEdge("b", "c", new Edge());
		topology.addEdge("b", "a", new Edge());
		assertEquals(2, topology.numberOfEdges());
	}
	
	@Test
	public void testNumberOfEdgesDirected() {
		Topology topology = new Topology(true);
		topology.addEdge("a", "b", new Edge());
		topology.addEdge("b", "c", new Edge());
		topology.addEdge("b", "a", new Edge());
		assertEquals(3, topology.numberOfEdges());
	}
}
