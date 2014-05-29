#include "edge.h"

namespace fnss {

Edge::Edge(const Quantity &capacity_, const Quantity &delay_,
			const float &weight_, const Quantity &bufferSize_) :
			capacity(capacity_), weight(weight_), delay(delay_),
			bufferSize(bufferSize_) {}

Quantity Edge::getCapacity() const {
	return this->capacity;
}

void Edge::setCapacity(const Quantity &capacity_) {
	this->capacity = capacity_;
}

float Edge::getWeight() const {
	return this->weight;
}

void Edge::setWeight(float weight_) {
	this->weight = weight_;
}

Quantity Edge::getDelay() const {
	return this->delay;
}

void Edge::setDelay(const Quantity &delay_) {
	this->delay = delay_;
}

Quantity Edge::getBufferSize() const {
	return this->bufferSize;
}

void Edge::setBufferSize(const Quantity &bufferSize_) {
	this->bufferSize = bufferSize_;
}

}
