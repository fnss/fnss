#include "event.h"

namespace fnss {

Event::Event(const Quantity &time) : time(time) {
	//this->time = time;
}

Quantity Event::getTime() const {
	return this->time;
}

void Event::setTime(const Quantity &time) {
	this->time = time;
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
