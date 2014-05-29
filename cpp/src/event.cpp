#include "event.h"

namespace fnss {

Event::Event(const Quantity &time_) : time(time_) {}

Quantity Event::getTime() const {
	return this->time;
}

void Event::setTime(const Quantity &time_) {
	this->time = time_;
}

bool Event::operator>(const Event &other) const {
	return this->time > other.time;
}

bool Event::operator>=(const Event &other) const {
	return this->time >= other.time;
}

bool Event::operator<(const Event &other) const {
	return this->time < other.time;
}

bool Event::operator<=(const Event &other) const {
	return this->time <= other.time;
}

}
