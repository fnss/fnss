import java.io.IOException;

import org.jdom2.JDOMException;

import uk.ac.ucl.ee.fnss.Pair;
import uk.ac.ucl.ee.fnss.Parser;
import uk.ac.ucl.ee.fnss.TrafficMatrix;
import uk.ac.ucl.ee.fnss.TrafficMatrixSequence;

/**
 * This example shows how to parse a traffic matrix sequence from an XML file
 * and read it.
 *
 */
public class ExampleTrafficMatrixSeq {

	public static void main(String[] args) {

		if (args.length != 1) {
			System.err.println("Usage: java ExampleTopology trafficMatrixSeqFile");
		}
		// parse path of topology XML file
		String trafficMatrixSeqFile = args[0];

		// parse topology from file
		TrafficMatrixSequence trafficMatrixSeq = null;
		try {
			trafficMatrixSeq = Parser.parseTrafficMatrixSequence(trafficMatrixSeqFile);
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
		
		System.out.println("Successfully parsed topology from file " + trafficMatrixSeqFile);
		
		// print number of matrices in the sequence
		int numberOfMatrices = trafficMatrixSeq.size();
		System.out.println("The TM sequence has " + numberOfMatrices +" matrices.");

		// let's extract the traffic volumes for each matrix
		// iterate over the matrices of the sequence
		for (TrafficMatrix matrix: trafficMatrixSeq) {
			System.out.println("Begin new traffic matrix");
			// get the unit of traffic volumes
			String volumeUnit = matrix.getVolumeUnit();
			// get the number of OD pairs
			int numberOfPairs = matrix.size();
			System.out.println("This traffic matrix has " + numberOfPairs + " OD pairs");
			// iterate over the OD pairs of the matrix
			for (Pair<String, String> odPair : matrix) {
				String origin = odPair.getU();
				String destination = odPair.getV();
				// get the traffic volume
				float volume = matrix.getFlow(origin, destination);
				System.out.println("From " + origin + " to " + destination + 
						": traffic volume: " + volume + " " + volumeUnit);
			}
		}
	}
}
