package uk.ac.ucl.ee.fnss;

import java.util.Iterator;
import java.util.List;
import java.util.Vector;

/**
 * Represent a sequence of traffic matrices, containing traffic matrices
 * referring to a sequence of time intervals.
 * 
 * @author Lorenzo Saino
 *
 */
public class TrafficMatrixSequence implements Iterable<TrafficMatrix> {

	private List<TrafficMatrix> trafficMatrices = new Vector<TrafficMatrix>();

	private String timeUnit = null;
	private int interval = 0;

	/**
	 * Constructor
	 */
	public TrafficMatrixSequence() { }

	/**
	 * Contructor
	 * 
	 * @param interval The time interval between subsequent traffic matrices
	 * @param timeUnit The unit of time of the interval value
	 */
	public TrafficMatrixSequence(int interval, String timeUnit) {
		if (!Units.isValidTimeUnit(timeUnit)) {
			throw new IllegalArgumentException(
					"The value of the timeUnit parameter is not valid");
		}
		this.interval = interval;
		this.timeUnit = timeUnit;
	}

	/**
	 * Return the number of traffic matrices in the sequence
	 * 
	 * @return The number of traffic matrices
	 */
	public int size() {
		return trafficMatrices.size();
	}
	
	/**
	 * Return the unit of time
	 * 
	 * @return the time unit
	 */
	public String getTimeUnit() {
		return timeUnit;
	}

	/**
	 * Set the unit of time
	 * 
	 * @param timeUnit the time unit to set
	 */
	public void setTimeUnit(String timeUnit) {
		this.timeUnit = timeUnit;
	}

	/**
	 * Return the time interval between subsequent matrices
	 * 
	 * @return the interval
	 */
	public int getInterval() {
		return interval;
	}

	/**
	 * Set the time interval between subsequent matrices
	 * 
	 * @param interval the interval to set
	 */
	public void setInterval(int interval) {
		this.interval = interval;
	}

	/**
	 * Append a matrix to the end of the sequence
	 * 
	 * @param trafficMatrix the traffic matrix to add
	 */
	public void addMatrix(TrafficMatrix trafficMatrix) {
		trafficMatrices.add(trafficMatrix);
	}
	
	/**
	 * Add a traffic matrix in a specific position of the sequence
	 * @param index the position in the sequence
	 * @param trafficMatrix the traffic matrix to add
	 */
	public void addMatrix(int index, TrafficMatrix trafficMatrix) {
		trafficMatrices.add(index, trafficMatrix);
	}
	
	/**
	 * Remove the specified traffic matrix from the sequence
	 * 
	 * @param trafficMatrix the matrix to remove
	 */
	public void removeMatrix(TrafficMatrix trafficMatrix) {
		trafficMatrices.remove(trafficMatrix);
	}

	/**
	 * Remove the traffic matrix in a specific position from the sequence
	 * 
	 * @param index the index of the matrix to removed
	 */
	public void removeMatrix(int index) {
		trafficMatrices.remove(index);
	}

	/**
	 * Return the traffic matrix in a specific point of he sequence
	 * @param index The index of the matrix
	 * @return The selected matrix
	 */
	public TrafficMatrix getMatrix(int index) {
		return trafficMatrices.get(index);
	}

	/**
	 * Return an iterator over the matrices of the sequence
	 * 
	 * @return the iterator
	 */
	@Override
	public Iterator<TrafficMatrix> iterator() {
		return trafficMatrices.iterator();
	}
}
