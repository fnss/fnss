package io.github.fnss;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

/**
 * Represent a traffic matrix (referring to a single time interval)
 * 
 * @author Lorenzo Saino
 *
 */
public class TrafficMatrix implements Iterable<Pair<String, String>> {

	private String volumeUnit = null;
	private Map<Pair<String, String>, Float> trafficMatrix =
			new Hashtable<Pair<String, String>, Float>();

	/**
	 * Constructor
	 * 
	 * @param volumeUnit the unit of traffic volumes
	 */
	public TrafficMatrix(String volumeUnit) {
		if (!Units.isValidCapacityUnit(volumeUnit)) {
			throw new IllegalArgumentException(
					"The value of the volumeUnit parameter is not valid");
		}
		trafficMatrix = new HashMap<Pair<String, String>, Float>();
		this.volumeUnit = volumeUnit;
	}

	/**
	 * Return the number of flows in the matrix
	 * 
	 * @return The number of flows in the matrix
	 */
	public int size() {
		return trafficMatrix.size();
	}
	
	/**
	 * Return the unit of traffic volumes
	 *
	 * @return the volume unit
	 */
	public String getVolumeUnit() {
		return volumeUnit;
	}

	/**
	 * Set the unit of traffic volumes
	 * 
	 * @param volumeUnit the volume unit to set
	 */
	public void setVolumeUnit(String volumeUnit) {
		if (!Units.isValidCapacityUnit(volumeUnit)) {
			throw new IllegalArgumentException(
					"The value of the volumeUnit parameter is not valid");
		}
		this.volumeUnit = volumeUnit;
	}
	
	/**
	 * Return the traffic volume of a specific flow
	 * 
	 * @param origin The origin of the flow
	 * @param destination The destination of the flow
	 * @return The volume of traffic
	 */
	public float getFlow(String origin, String destination) {
		try {
			return trafficMatrix.get(
					new Pair<String, String>(origin, destination));
		} catch(NullPointerException e) {
			return 0;
		}
	}

	/**
	 * Add a flow to the matrix
	 * 
	 * @param volume The volume of traffic
	 * @param origin The origin of the flow
	 * @param destination The destination of the flow
	 */
	public void addFlow(String origin, String destination, float volume) {
		trafficMatrix.put(
				new Pair<String, String>(origin, destination), volume);
	}

	/**
	 * Remove a flow from the matrix
	 * 
	 * @param origin The origin of the flow
	 * @param destination The destination of the flow
	 */
	public void removeFlow(String origin, String destination) {
		trafficMatrix.remove(new Pair<String, String>(origin, destination));
	}

	/**
	 * Return a pair of all origin-destination (OD) pairs of the matrix
	 * 
	 * @return a Set of OD pairs
	 */
	public Set<Pair<String, String>> getODPairs() {
		return trafficMatrix.keySet();
	}

	/**
	 * Return a set containing all traffic origins of the matrix
	 * 
	 * @return the traffic origins
	 */
	public Set<String> getOrigins() {
		Set<String> origins = new HashSet<String>();
		for (Pair<String, String> odPair : getODPairs()) {
			origins.add(odPair.getU());
		}
		return origins;
	}

	/**
	 * Return a set containing all traffic destinations of the matrix
	 * 
	 * @return the traffic destinations
	 */
	public Set<String> getDestinations() {
		Set<String> destinations = new HashSet<String>();
		for (Pair<String, String> odPair : getODPairs()) {
			destinations.add(odPair.getV());
		}
		return destinations;
	}

	/**
	 * Return an iterator over the OD pairs of matrix
	 * 
	 * @return the iterator
	 */
	@Override
	public Iterator<Pair<String, String>> iterator() {
		return getODPairs().iterator();
	}

}
