import io.github.fnss.Application;
import io.github.fnss.Edge;
import io.github.fnss.Node;
import io.github.fnss.Pair;
import io.github.fnss.Parser;
import io.github.fnss.ProtocolStack;
import io.github.fnss.Topology;

import java.io.IOException;

import org.jdom2.JDOMException;


/**
 * This example shows how to parse a traffic matrix sequence from an XML file
 * and read it.
 */
public class ExampleTopology {

	public static void main(String[] args) {

		if (args.length != 1) {
			System.err.println("Usage: java ExampleTopology topologyFile");
		}
		// parse path of topology XML file
		String topologyFile = args[0];

		// parse topology from file
		Topology  topology = null;
		try {
			topology = Parser.parseTopology(topologyFile);
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
		
		System.out.println("Successfully parsed topology from file " + topologyFile);
		
		// Print number of nodes and number of links
		int numberOfNodes = topology.numberOfNodes();
		int numberOfEdges = topology.numberOfEdges();
		System.out.println("The topology has " + numberOfNodes +" nodes and " 
					+ numberOfEdges + " links");

		// Let's extract capacity and delays from links.
		// First see the unit in which capcities are expressed (e.g. Mbps, Gbps etc..)
		String capacityUnit = topology.getCapacityUnit();
		// Now let's see the delay unit (e.g. ms, sec)
		String delayUnit = topology.getDelayUnit();
		// Now we extract and print all capacities and delays, by iterating through edges
		for (Pair<String, String> endpoints : topology.getAllEdges()) {
			Edge edge = topology.getEdge(endpoints);
			float capacity = edge.getCapacity();
			float delay = edge.getDelay();
			System.out.println("The link from " + endpoints.getU() + " to " +
							   endpoints.getV() +" has capacity " + capacity +
							   " " + capacityUnit + " and delay " + delay + " "
							   + delayUnit);
		}
		
		//Now let's get the stack and applications from all nodes
		for (String nodeId : topology.getAllNodes()) {
			Node node = topology.getNode(nodeId);
			ProtocolStack stack = node.getProtocolStack();
			if (stack != null) {
				String stackName = stack.getName();
				System.out.println("The node " + nodeId + " has a protocol stack named " 
									+ stackName + "  which has the following properties:");
				for (String propName : stack.getAllProperties()) {
					String propVal = stack.getProperty(propName);
					System.out.println("\tName: " + propName + ", value: " + propVal);
				}
			}
			
			for (String applicationName : node.getAllApplications()) {
				Application application = node.getApplication(applicationName);
				// Now let's get all properties of this stack
				System.out.println("The application " + applicationName + " on node " + 
								   nodeId + " has the following properties:");
				for (String propName : application.getAllProperties()) {
					String propVal = application.getProperty(propName);
					System.out.println("\tName: " + propName + ", value: " + propVal);
				}
			}
		}
	}
}
