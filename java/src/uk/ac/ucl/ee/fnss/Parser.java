package uk.ac.ucl.ee.fnss;

import java.io.IOException;
import java.util.List;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;

/**
 * Provides methods to parse FNSS output XML files and convert them in Java object.
 * 
 * @author Lorenzo Saino
 *
 */
public class Parser {
	
	// override constructor to prevent instantiation
	private Parser() { }
	
	/**
	 * Parse a topology XML file
	 * 
	 * @param topologyFile The name of the topology file
	 * @return A <code>Topology</code> object of the parsed topology
	 * @throws JDOMException If the XML file is badly formatted
	 * @throws IOException If an error occurs while trying to read the file
	 */
	public static Topology parseTopology(String topologyFile)
			throws JDOMException, IOException {
		Topology topology = null;
		SAXBuilder builder = new SAXBuilder();
		Document document = (Document) builder.build(topologyFile);
		Element rootNode = document.getRootElement();
		String linkDefault = rootNode.getAttributeValue("linkdefault");
		if (linkDefault.equals("directed")) {
			topology = new Topology(true);
		} else {
			topology = new Topology(false);
		}
		List<Element> properties = rootNode.getChildren("property");
		for (Element propertyElement: properties) {
			String name = propertyElement.getAttributeValue("name");
			String value = propertyElement.getTextTrim();
			if (name.equals("capacity_unit")) {
				topology.setCapacityUnit(value);
			} else if (name.equals("delay_unit")) {
				topology.setDelayUnit(value);
			} else if (name.equals("distance_unit")) {
				topology.setDistanceUnit(value);
			} else if (name.equals("buffer_unit")) {
				topology.setBufferUnit(value);
			} else {
				topology.setProperty(name, value);
			}
		}
		List<Element> nodes = rootNode.getChildren("node");
		for (Element nodeElement: nodes) {
			String nodeName = nodeElement.getAttributeValue("id");
			Node node = new Node();
			List<Element> nodeProperties = nodeElement.getChildren("property");
			for (Element propertyElement: nodeProperties) {
				String name = propertyElement.getAttributeValue("name");
				String value = propertyElement.getTextTrim();
				node.setProperty(name, value);
			}
			// there can only be one stack
			Element stackElement = nodeElement.getChild("stack");
			if (stackElement != null) {
				String stackName = stackElement.getAttributeValue("name");
				ProtocolStack stack = new ProtocolStack(stackName);
				List<Element> stackProperties = stackElement.getChildren("property");
				for (Element propertyElement: stackProperties) {
					String name = propertyElement.getAttributeValue("name");
					String value = propertyElement.getTextTrim();
					stack.setProperty(name, value);
				}
				node.setProtocolStack(stack);
			}
			List<Element> nodeApplications = nodeElement.getChildren("application");
			for (Element applicationElement : nodeApplications) {
				String applicationName = applicationElement.getAttributeValue("name");
				Application application = new Application(applicationName);
				List<Element> applicationProperties = applicationElement.getChildren("property");
				for (Element propertyElement: applicationProperties) {
					String name = propertyElement.getAttributeValue("name");
					String value = propertyElement.getTextTrim();
					application.setProperty(name, value);
				}
				node.setApplication(application);
			}
			topology.addNode(nodeName, node);
		}

		List<Element> edges = rootNode.getChildren("link");
		for (Element edgeElement: edges) {
			Edge edge = new Edge();
			String u = edgeElement.getChildText("from");
			String v = edgeElement.getChildText("to");
			List<Element> edgeProperties = edgeElement.getChildren("property");
			for (Element propertyElement: edgeProperties) {
				String name = propertyElement.getAttributeValue("name");
				String value = propertyElement.getTextTrim();
				if (name.equals("capacity")) {
					edge.setCapacity(Float.parseFloat(value));
				} else if (name.equals("delay")) {
					edge.setDelay(Float.parseFloat(value));
				} else if (name.equals("weight")) {
					edge.setWeight(Float.parseFloat(value));
				} else if (name.equals("buffer")) {
					edge.setBufferSize(Float.parseFloat(value));
				} else {
					edge.setProperty(name, value);
				}
			}
			topology.addEdge(u, v, edge);
		}
		return topology;
	}

	/**
	 * Parse an event schedule XML file
	 *
	 * @param eventScheduleFile The name of the event schedule file
	 * @return An <code>EventSchudule</code> object of the parsed event
	 * schedule
	 * @throws JDOMException If the XML file is badly formatted
	 * @throws IOException If an error occurs while trying to read the file
	 */
	public static EventSchedule parseEventSchedule(String eventScheduleFile)
			throws JDOMException, IOException {
		EventSchedule eventSchedule = null;
		String timeUnit = null;
		float startTime = -1;
		float endTime = -1;

		SAXBuilder builder = new SAXBuilder();
		Document document = (Document) builder.build(eventScheduleFile);
		Element rootNode = document.getRootElement();

		List<Element> properties = rootNode.getChildren("property");
		for (Element propertyElement: properties) {
			String name = propertyElement.getAttributeValue("name");
			String value = propertyElement.getTextTrim();
			if (name.equals("t_unit")) {
				timeUnit = value;
			} else if (name.equals("t_start")) {
				startTime = Float.parseFloat(value);
			} else if (name.equals("t_end")) {
				endTime = Float.parseFloat(value);
			} else {
				// If format is extended and new properties are added 
				// put here the code to handle them
				continue;
			}
		}
		eventSchedule = new EventSchedule(timeUnit, startTime, endTime);
		List<Element> events = rootNode.getChildren("event");
		for (Element eventElement: events) {
			float time = Float.parseFloat(eventElement.getAttributeValue("time"));
			Event event = new Event(time, timeUnit);
			List<Element> eventProperties = eventElement.getChildren("property");
			for (Element propertyElement: eventProperties) {
				String name = propertyElement.getAttributeValue("name");
				String value = propertyElement.getTextTrim();
				event.setProperty(name, value);
			}
			eventSchedule.addEvent(event);
		}
		return eventSchedule;
	}

	/**
	 * Parse a traffic matrix file containing a single traffic matrix
	 * 
	 * @param trafficMatrixFile The name of the traffic matrix file
	 * @return A <code>TrafficMatrix</code> object of the parsed matrix
	 * @throws JDOMException If the XML file is badly formatted
	 * @throws IOException If an error occurs while trying to read the file
	 */
	public static TrafficMatrix parseTrafficMatrix(String trafficMatrixFile)
			throws JDOMException, IOException {
		return parseTrafficMatrixSequence(trafficMatrixFile).getMatrix(0);
	}

	/**
	 * Parse a traffic matrix file containing a sequence of traffic matrices
	 *
	 * @param trafficMatrixFile The name of the traffic matrix file
	 * @return A <code>TrafficMatrixSequence</code>  object containing a
	 * sequence of <code>TrafficMatrix</code> objects
	 * @throws JDOMException If the XML file is badly formatted
	 * @throws IOException If an error occurs while trying to read the file
	 */
	@SuppressWarnings("unused")
	public static TrafficMatrixSequence parseTrafficMatrixSequence(
			String trafficMatrixFile) throws JDOMException, IOException {
		TrafficMatrixSequence trafficMatrixSequence = null;
		String timeUnit = null;
		int interval = -1;
		
		String name = null;
		String type = null;
		String value = null;

		SAXBuilder builder = new SAXBuilder();
		Document document = (Document) builder.build(trafficMatrixFile);
		Element rootNode = document.getRootElement();

		List<Element> properties = rootNode.getChildren("property");
		for (Element propertyElement: properties) {
			name = propertyElement.getAttributeValue("name");
			type = propertyElement.getAttributeValue("type");
			value = propertyElement.getTextTrim();
			if (name.equals("t_unit")) {
				timeUnit = value;
			} else if (name.equals("interval")) {
				interval = Integer.parseInt(value);
			} else {
				// If format is extended and new properties are added
				// put here the code to handle them
				continue;
			}
		}
		if (interval > 0 && timeUnit != null) {
			trafficMatrixSequence = new TrafficMatrixSequence(
					interval, timeUnit);
		} else {
			trafficMatrixSequence = new TrafficMatrixSequence();
		}
		List<Element> trafficMatrices = rootNode.getChildren("time");
		for (Element tmElement: trafficMatrices) {
			TrafficMatrix trafficMatrix = new TrafficMatrix();
			List<Element> tmProperties = tmElement.getChildren("property");
			for (Element tmPropertyElement: tmProperties) {
				name = tmPropertyElement.getAttributeValue("name");
				type = tmPropertyElement.getAttributeValue("type");
				value = tmPropertyElement.getTextTrim();
				if (name.equals("volume_unit")) {
					trafficMatrix.setVolumeUnit(value);
				} else {
					// If format is extended and new properties are added
					// put here the code to handle them
					continue;
				}
			}
			List<Element> origins = tmElement.getChildren("origin");
			for (Element originElement: origins) {
				String o = originElement.getAttributeValue("id");
				List<Element> destinations = originElement.getChildren("destination");
				for (Element destinationElement: destinations) {
					String d = destinationElement.getAttributeValue("id");
					float load = Float.parseFloat(destinationElement.getValue());
					trafficMatrix.addFlow(o, d, load);
				}
			}
			trafficMatrixSequence.addMatrix(trafficMatrix);
		}
		return trafficMatrixSequence;
	}

}
