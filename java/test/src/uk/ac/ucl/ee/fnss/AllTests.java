package uk.ac.ucl.ee.fnss;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;

@RunWith(Suite.class)

@SuiteClasses({ TopologyTest.class, 
				EventScheduleTest.class, 
				TrafficMatrixTest.class,
				ParserTest.class})

public class AllTests { }
