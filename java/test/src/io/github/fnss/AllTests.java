package io.github.fnss;

import io.github.fnss.ext.jgrapht.JGraphTConverterTest;
import io.github.fnss.ext.jung.JUNGConverterTest;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;


@RunWith(Suite.class)

@SuiteClasses({ TopologyTest.class, 
				EventScheduleTest.class, 
				TrafficMatrixTest.class,
				ParserTest.class,
				JGraphTConverterTest.class,
				JUNGConverterTest.class
				})

public class AllTests { }
