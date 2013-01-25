import java.io.IOException;

import org.jdom2.JDOMException;

import uk.ac.ucl.ee.fnss.Event;
import uk.ac.ucl.ee.fnss.EventSchedule;
import uk.ac.ucl.ee.fnss.Parser;

/**
 * This example shows how to parse an event schedule from an XML file
 * and read it.
 */
public class ExampleEventSchedule {

	public static void main(String[] args) {

		if (args.length != 1) {
			System.err.println("Usage: java ExampleEventSchedule eventScheduleFile");
		}
		// parse path of event schedule XML file
		String eventScheduleFile = args[0];
		
		// parse the event schedule from file
		EventSchedule eventSchedule = null;
		try {
			eventSchedule = Parser.parseEventSchedule(eventScheduleFile);
		} catch (JDOMException e) {
			// thrown if XML is badly formatted
			e.printStackTrace();
			System.exit(1);
		} catch (IOException e) {
			// thrown if problems occur while reading file, e.g. the file
			// doens't exist or you don't have the authorization to read it
			e.printStackTrace();
			System.exit(1);
		}
		
		// get number of events
		int numberOfEvents = eventSchedule.size();
		System.out.println("The schedule has " + numberOfEvents + " events");
		
		// get unit in which event times are expressed
		String timeUnit = eventSchedule.getTimeUnit();
		
		// get start and end time of the schedule
		float startTime = eventSchedule.getStartTime();
		float endTime = eventSchedule.getEndTime();
		System.out.println("The event schedule starts at " +startTime + " " + timeUnit +
				" and ends at " + endTime + " " + timeUnit);
		
		System.out.println("Events of the schedule:");
		for (Event event : eventSchedule) {
			float time = event.getTime();
			System.out.println("Event at time: " + time + " " + timeUnit + ". Properties:");
			for (String propName : event.getAllProperties()) {
				String propVal = event.getProperty(propName);
				System.out.println("\tName: " + propName + ", value: " + propVal);
			}
		}
	}

}
