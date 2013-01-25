package uk.ac.ucl.ee.fnss;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;


public class EventScheduleTest {
	
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
		EventSchedule es = new EventSchedule("sec", 12, 30);
		assertEquals("sec", es.getTimeUnit());
		assertEquals(12, es.getStartTime(), 0.1);
		assertEquals(30, es.getEndTime(), 0.1);
	}


}
