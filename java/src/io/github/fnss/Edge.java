package io.github.fnss;

/**
 * Represent an edge of a topology
 *
 * @author Lorenzo Saino
 *
 * @see Topology
 *
 */
public class Edge extends PropertyContainer implements Cloneable {

	private float capacity = -1;
	private float weight = 1;
	private float delay = 0;
	private float bufferSize = - 1;
	private float length = 0;

	/**
	 * Constructor
	 */
	public Edge() { }
	
	/**
	 * Return the capacity of the link. The capacity is returned without unit.
	 * To get the capacity unit, invoke the method getCapacityUnit() of the
	 * Topology object to which this edge is associated.
	 *
	 * @return the capacity
	 *
	 * @see Topology#getCapacityUnit()
	 */
	public float getCapacity() {
		return capacity;
	}

	/**
	 * Set the capacity of the link
	 * 
	 * @param capacity the capacity to set
	 */
	public void setCapacity(float capacity) {
		this.capacity = capacity;
	}

	/**
	 * Return the weight of the link
	 *
	 * @return the weight
	 */
	public float getWeight() {
		return weight;
	}

	/**
	 * Set the weight of the link
	 * 
	 * @param weight the weight to set
	 */
	public void setWeight(float weight) {
		this.weight = weight;
	}

	/**
	 * Return the delay of the link, without the time unit.
	 * To get the time unit of the delay use the parent Topology
	 * object's getDelayUnit() method.
	 * 
	 * @return the delay
	 * 
	 * @see Topology#getDelayUnit()
	 */
	public float getDelay() {
		return delay;
	}

	/**
	 * Set the link delay
	 * 
	 * @param delay the delay to set
	 */
	public void setDelay(float delay) {
		this.delay = delay;
	}

	/**
	 * Get the size of the buffer associated to this link
	 * 
	 * @return the bufferSize
	 * 
	 * @see Topology#getBufferUnit()
	 */
	public float getBufferSize() {
		return bufferSize;
	}

	/**
	 * Set the size of the buffer associated to this link
	 * 
	 * @param bufferSize the bufferSize to set
	 */
	public void setBufferSize(float bufferSize) {
		this.bufferSize = bufferSize;
	}
	
	/**
	 * Return the length of the link
	 *
	 * @return the length
	 */
	public float getLength() {
		return length;
	}

	/**
	 * Set the length of the link
	 * 
	 * @param length the length to set
	 */
	public void setLength(float length) {
		this.length = length;
	}
	/**
	 * Return a copy of this object
	 * 
	 * @return A copy of this object
	 */
	@Override
	public Edge clone() {
		return (Edge) super.clone();
	}

}
