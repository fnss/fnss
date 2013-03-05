#include "edge.h"

namespace fnss {

Edge::Edge(const Quantity &capacity, const Quantity &delay,
			const float &weight, const Quantity &bufferSize) :
			capacity(capacity), delay(delay), bufferSize(bufferSize){
	this->weight = weight;
}

Quantity Edge::getCapacity() const {
	return this->capacity;
}

void Edge::setCapacity(const Quantity &capacity) {
	this->capacity = capacity;
}

float Edge::getWeight() const {
	return this->weight;
}

void Edge::setWeight(float weight) {
	this->weight = weight;
}

Quantity Edge::getDelay() const {
	return this->delay;
}

void Edge::setDelay(const Quantity &delay) {
	this->delay = delay;
}

Quantity Edge::getBufferSize() const {
	return this->bufferSize;
}

void Edge::setBufferSize(const Quantity &bufferSize) {
	this->bufferSize = bufferSize;
}

}
