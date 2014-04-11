package io.github.fnss;

import java.util.Iterator;
import java.util.List;
import java.util.Vector;

/**
 * Represent a schedule of events. Each event is represented by a time and a
 * set of properties.
 *
 * @author Lorenzo Saino
 *
 */
public class EventSchedule implements Iterable<Event> {

	/*
	 * Implement eventSchedule as Vector rather than ArrayList to make it
	 * thread-safe.
	 */
	private List<Event> eventSchedule = new Vector<Event>();
	private String timeUnit = null;
	private float startTime = 0;
	private float endTime = 0;

	/**
	 * Constructor
	 * 
	 * @param timeUnit The unit of time of the event
	 * @param startTime The start time of the schedule
	 * @param endTime The end time of the schedule
	 */
	public EventSchedule(String timeUnit, float startTime, float endTime) {
		if (endTime < startTime) {
			throw new IllegalArgumentException(
					"endTime cannot be lower than startTime");
		}
		if (!Units.isValidTimeUnit(timeUnit)) {
			throw new IllegalArgumentException(
					"The value of the timeUnit parameter is not valid");
		}
		this.timeUnit = timeUnit;
		this.startTime = startTime;
		this.endTime = endTime;
	}

	/**
	 * Return the unit of time
	 * 
	 * @return timeUnit the unit of time
	 */
	public String getTimeUnit() {
		return timeUnit;
	}

	/**
	 * Set the unit of time
	 * 
	 * @param timeUnit the unit of time
	 */
	public void setTimeUnit(String timeUnit) {
		this.timeUnit = timeUnit;
	}

	/**
	 * Return the start time of the event schedule
	 * 
	 * @return the startTime of the event schedule
	 */
	public float getStartTime() {
		return startTime;
	}

	/**
	 * Set the start time of the event schedule
	 * 
	 * @param startTime the start time
	 */
	public void setStartTime(long startTime) {
		this.startTime = startTime;
	}

	/**
	 * Return the end time of the event schedule
	 * 
	 * @return the endTime
	 */
	public float getEndTime() {
		return endTime;
	}

	/**
	 * Set the end time of the event schedule
	 * 
	 * @param endTime the endTime to set
	 */
	public void setEndTime(long endTime) {
		this.endTime = endTime;
	}
	
	/**
	 * Add an event to the schedule
	 * 
	 * @param event The Event object to add to the schedule
	 */
	public void addEvent(Event event) {
		eventSchedule.add(event);
	}
	
	/**
	 * Add an event to the schedule
	 * 
	 * @param i The index of the Event object to remove
	 */
	public void removeEvent(int i) {
		eventSchedule.remove(i);
	}
	
	/**
	 * Remove an event from the schedule
	 * 
	 * @param event The Event object to remove
	 */
	public void removeEvent(Event event) {
		eventSchedule.remove(event);
	}
	
	/**
	 * Return the i-th event of the schedule
	 * 
	 * @param i the index of the Event object
	 * @return the event with index <code>i</code>
	 */
	public Event getEvent(int i) {
		return eventSchedule.get(i);
	}
	
	/**
	 * Return the number of events in the schedule
	 * 
	 * @return the number of events in the schedule
	 */
	public int size() {
		return eventSchedule.size();
	}
	
    /**
     * Returns an iterator over the events of the schedule.
     *
     * @return an Iterator.
     */
	@Override
	public Iterator<Event> iterator() {
		return eventSchedule.iterator();
	}
		
}
