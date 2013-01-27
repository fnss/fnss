#ifndef EVENT_SCHEDULE_H
#define EVENT_SCHEDULE_H

#include "event.h"
#include "quantity.h"
#include "units.h"

#include <vector>
#include <exception>
#include <sstream>

namespace fnss {

/**
 * Represent a schedule of events. Each event is represented by a time and a set
 * of properties.
 * 
 * @author Cosmin Cocora
 *
 */
class EventSchedule {
public:
	/**
	 * Constructor.
	 *
	 * @param startTime the start time of the schedule.
	 * @param endTime the end time of the schedule.
	 */
	EventSchedule(const Quantity &startTime = Quantity("0s", Units::Time),
					const Quantity &endTime = Quantity("0s", Units::Time));

	/**
	 * Get the start time of the schedule.
	 * 
	 * @return the start time of the schedule.
	 */
	Quantity getStartTime() const;

	/**
	 * Get the start time of the schedule.
	 * 
	 * @param time the start time of the schedule.
	 */
	void setStartTime(const Quantity &time);

	/**
	 * Get the end time of the schedule.
	 * 
	 * @return the end time of the schedule.
	 */
	Quantity getEndTime() const;

	/**
	 * Get the end time of the schedule.
	 * 
	 * @param time the end time of the schedule.
	 */
	void setEndTime(const Quantity &time);

	/**
	 * Get the number of events present in the schedule.
	 *
	 * @return the number of events.
	 */
	unsigned int size() const;

	/**
	 * Get a copy of the i-th \c Event in the schedule.
	 * 
	 * The events are sorted in ascending order by time.
	 * Throws an exception if the index is out-of-bounds.
	 *
	 * @param index the index of the \c Event to get.
	 * @return a copy of the i-th \c Event.
	 */
	Event getEvent(unsigned int index) const;

	/**
	 * Add an \c Event to the schedule.
	 *
	 * @param event the \c Event to add.
	 */
	void addEvent(const Event &event);

	/**
	 * Remove the i-th \c Event from the schedule.
	 * 
	 * The events are sorted in ascending order by time.
	 * The method does nothing if the given index is out of bounds.
	 * 
	 * @param index the index of the \c Event to remove.
	 */
	void removeEvent(unsigned int index);

	class IndexOutOfBoundsException : public std::exception {
	public:
		IndexOutOfBoundsException(unsigned int index) throw() {
			std::stringstream ss;
			ss<<"The EventSchedule index "<<index<<" was out-of-bounds.";
			this->exceptionStr = ss.str();
		}

		~IndexOutOfBoundsException() throw() {
		}

		const char* what() const throw() {
			return this->exceptionStr.c_str();
		}

	private:
		std::string exceptionStr;
	};

private:
	Quantity startTime;
	Quantity endTime;
	typedef std::vector<Event> scheduleType;
	scheduleType schedule;
};

} //namespace

#endif //EVENT_SCHEDULE_H