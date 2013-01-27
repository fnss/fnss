#include "event-schedule.h"

#include <algorithm>

namespace fnss {

EventSchedule::EventSchedule(const Quantity &startTime, const Quantity &endTime) :
				startTime(startTime), endTime(endTime) {

}

Quantity EventSchedule::getStartTime() const {
	return this->startTime;
}

void EventSchedule::setStartTime(const Quantity &time) {
	this->startTime = time;
}

Quantity EventSchedule::getEndTime() const {
	return this->endTime;
}

void EventSchedule::setEndTime(const Quantity &time) {
	this->endTime = time;
}

unsigned int EventSchedule::size() const {
	return this->schedule.size();
}

Event EventSchedule::getEvent(unsigned int index) const {
	if(index >= this->schedule.size())
		throw IndexOutOfBoundsException(index);

	return this->schedule[index];
}

void EventSchedule::addEvent(const Event &event) {
	this->schedule.push_back(event);
	std::sort(this->schedule.begin(), this->schedule.end());
}

void EventSchedule::removeEvent(unsigned int index) {
	if(index >= this->schedule.size())
		throw IndexOutOfBoundsException(index);

	scheduleType::iterator it = this->schedule.begin() + index;
	this->schedule.erase(it);
}

} //namespace