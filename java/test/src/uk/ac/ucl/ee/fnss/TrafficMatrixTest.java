package uk.ac.ucl.ee.fnss;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

public class TrafficMatrixTest {

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
	public void testGetOriginsDestinations() {
		TrafficMatrix tm = new TrafficMatrix();
		tm.addFlow("a", "b", 1);
		tm.addFlow("a", "c", 1);
		tm.addFlow("b", "c", 1);
		assertEquals(tm.getOrigins().size(), 2);
		assertTrue(tm.getOrigins().contains("a"));
		assertTrue(tm.getOrigins().contains("b"));
		assertEquals(tm.getDestinations().size(), 2);
		assertTrue(tm.getDestinations().contains("b"));
		assertTrue(tm.getDestinations().contains("c"));
	}
	
	@Test
	public void testAddRemoveFlows() {
		TrafficMatrix tm = new TrafficMatrix();
		tm.addFlow("a", "b", 1);
		tm.addFlow("b", "a", 4);
		tm.addFlow("a", "c", 2);
		tm.addFlow("b", "c", 3);
		assertEquals(1, tm.getFlow("a", "b"), 0.01);
		assertEquals(4, tm.getFlow("b", "a"), 0.01);
		assertEquals(0, tm.getFlow("c", "a"), 0.01);
		tm.removeFlow("a", "b");
		assertEquals(0, tm.getFlow("a", "b"), 0.01);
		assertNotNull(tm.getFlow("b", "a"));
	}
	
	@Test
	public void testGetODPairs() {
		TrafficMatrix tm = new TrafficMatrix();
		tm.addFlow("a", "b", 1);
		tm.addFlow("b", "a", 4);
		tm.addFlow("a", "c", 2);
		tm.addFlow("b", "c", 3);
		assertEquals(4, tm.getODPairs().size());
	}

}
