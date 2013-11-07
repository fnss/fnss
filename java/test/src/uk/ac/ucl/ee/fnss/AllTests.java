package uk.ac.ucl.ee.fnss;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;

import uk.ac.ucl.ee.fnss.ext.jgrapht.JGraphTConverterTest;
import uk.ac.ucl.ee.fnss.ext.jung.JUNGConverterTest;

@RunWith(Suite.class)

@SuiteClasses({ TopologyTest.class, 
				EventScheduleTest.class, 
				TrafficMatrixTest.class,
				ParserTest.class,
				JGraphTConverterTest.class,
				JUNGConverterTest.class
				})

public class AllTests { }
