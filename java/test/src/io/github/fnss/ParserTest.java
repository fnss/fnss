package io.github.fnss;

import static org.junit.Assert.*;

import io.github.fnss.EventSchedule;
import io.github.fnss.Parser;
import io.github.fnss.Topology;
import io.github.fnss.Units;

import java.io.File;
import java.io.IOException;

import org.jdom2.JDOMException;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

public class ParserTest {

	private static String resourcesDir = null;
	
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
		resourcesDir = System.getProperty("test.res.dir");
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
	public void testParseTopology() {
		try {
			Topology topology = Parser.parseTopology
					(resourcesDir + File.separator + "topology.xml");
			assertNotNull(topology);
			assertEquals(10, topology.numberOfNodes());
			assertEquals(18, topology.numberOfEdges());
			assertEquals(Units.CAPACITY_MEGABIT_PER_SEC, topology.getCapacityUnit());
			assertEquals(Units.DELAY_MILLISECONDS, topology.getDelayUnit());
			assertEquals("er", topology.getProperty("type"));
			
			assertEquals("99.76", topology.getNode("2").getProperty("longitude"));
			
			assertEquals(20.77, topology.getEdge("1", "5").getCapacity(), 0.1);
			assertEquals(20.77, topology.getEdge("5", "1").getCapacity(), 0.1);
			assertEquals(30, topology.getEdge("5", "1").getBufferSize(), 0.1);
			assertEquals("backbone", topology.getEdge("5", "1").getProperty("type"));
			
			assertEquals("tcp", topology.getNode("2").getProtocolStack().getName());
			assertEquals("cubic", topology.getNode("2").getProtocolStack().getProperty("protocol"));
			assertEquals(2, topology.getNode("2").getAllApplications().size());
			assertTrue(topology.getNode("2").getAllApplications().contains("server"));
			assertTrue(topology.getNode("2").getAllApplications().contains("client"));
			assertEquals("80", topology.getNode("2").getApplication("server").getProperty("port"));
		} catch (JDOMException e) {
			fail("Cannot parse correctly topology file");
		} catch (IOException e) {
			fail("Cannot read the input topology file");
		}
	}

	@Test
	public void testParseEventSchedule() {
		try {
			EventSchedule eventSchedule = Parser.parseEventSchedule
					(resourcesDir + File.separator + "eventschedule.xml");
			assertNotNull(eventSchedule);
		} catch (JDOMException e) {
			fail("Cannot parse correctly event schedule file");
		} catch (IOException e) {
			fail("Cannot read the input event schedule file");
		}
	}

	@Test
	public void testParseTrafficMatrix() {
	}

	@Test
	public void testParseTrafficMatrixSequence() {
	}

}
