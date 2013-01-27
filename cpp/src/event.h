#ifndef EVENT_H
#define EVENT_H

#include "property-container.h"
#include "quantity.h"
#include "units.h"

#include <string>

namespace fnss {

/**
 * Represent an event of an event schedule
 * 
 * @author Cosmin Cocora
 *
 */
class Event : public PropertyContainer {
public:
	/**
	 * Constructor.
	 *
	 * @param time the time at which the event occurs.
	 */
	Event(const Quantity &time = Quantity("0sec", Units::Time));

	/**
	 * Get method for the scheduled time of the event.
	 *
	 * @return the time at which the event occurs.
	 */
	Quantity getTime() const;

	/**
	 * Set method for the event's scheduled time.
	 *
	 * @param time the time at which the event occurs.
	 */
	void setTime(const Quantity &time);

	bool operator>(const Event &other) const;
	bool operator>=(const Event &other) const;
	bool operator<(const Event &other) const;
	bool operator<=(const Event &other) const;

private:
	Quantity time;	//The scheduled time of the event.

};

} //namespace

#endif //EVENT_H