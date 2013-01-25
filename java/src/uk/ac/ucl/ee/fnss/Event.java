package uk.ac.ucl.ee.fnss;

/**
 * Represent an event of an event schedule
 *
 * @author Lorenzo Saino
 *
 */
public class Event extends PropertyContainer implements Comparable<Event> {

	private float time = 0;
	private String timeUnit = null;

	/**
	 * Constructor
	 * 
	 * @param time The time at which the event occurs
	 * @param timeUnit The unit of time values.
	 */
	public Event(float time, String timeUnit) {
		if (!Units.isValidTimeUnit(timeUnit)) {
			throw new IllegalArgumentException
					("The provided timeUnit parameter is invalid");
		}
		this.time = time;
		this.timeUnit = timeUnit;
	}
	
	/**
	 * Return the time at which the event occurs
	 * 
	 * @return the time
	 */
	public float getTime() {
		return time;
	}
	
	/**
	 * Set the time at which the event occurs
	 * 
	 * @param time
	 */
	public void setTime(float time) {
		this.time = time;
	}
	
	/**
	 * Return the unit of the event time
	 * 
	 * @return the unit of time
	 */
	public String getTimeUnit() {
		return timeUnit;
	}
	
	/**
	 * Set the unit of the event time
	 * 
	 * @param timeUnit the unit of time
	 */
	public void setTimeUnit(String timeUnit) {
		if (!Units.isValidTimeUnit(timeUnit)) {
			throw new IllegalArgumentException
					("The provided timeUnit parameter is invalid");
		}
		this.timeUnit = timeUnit;
	}
	
	/**
	 * Compares this object with the specified object for order.  Returns a
     * negative integer, zero, or a positive integer as this object is less
     * than, equal to, or greater than the specified object.
     * 
     * @return -1, 0 or 1
	 */
	@Override
	public int compareTo(Event o) {
		float comparedTime = 0;
		if (this.timeUnit.equals(o.getTimeUnit())) {
			comparedTime = o.getTime();
		} else {
			comparedTime = Units.convertTimeValue(o.getTime(), o.getTimeUnit(),
					this.timeUnit);
		}
		if (this.getTime() == comparedTime) {
			return 0;
		} else if (this.getTime() > comparedTime) {
			return 1;
		} else if (this.getTime() < comparedTime) {
			return -1;
		} else {
			// Should never be thrown
			throw new IllegalArgumentException(
					"The two objects are not comparable");
		}
	}
	
}
