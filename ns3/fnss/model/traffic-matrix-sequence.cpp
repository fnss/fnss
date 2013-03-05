#include "traffic-matrix-sequence.h"

namespace fnss {

TrafficMatrixSequence::TrafficMatrixSequence(const Quantity &interval) :
												interval(interval) {

}

Quantity TrafficMatrixSequence::getInterval() const {
	return this->interval;
}

void TrafficMatrixSequence::setInterval(const Quantity &interval) {
	this->interval = interval;
}

unsigned int TrafficMatrixSequence::size() const {
	return this->sequence.size();
}

void TrafficMatrixSequence::addMatrix(const TrafficMatrix &matrix) {
	this->sequence.push_back(matrix);
}

void TrafficMatrixSequence::addMatrix(const TrafficMatrix &matrix,
									unsigned int index) {
	if(index >= this->sequence.size())
		this->sequence.resize(index + 1);

	this->sequence[index] = matrix;
}

void TrafficMatrixSequence::removeMatrix(unsigned int index) {
	if(index >= this->sequence.size())
		throw IndexOutOfBoundsException(index);

	sequenceType::iterator it = this->sequence.begin() + index;
	if(it == this->sequence.end() - 1)
		this->sequence.erase(it);
	else
		this->sequence[index] = TrafficMatrix();
}

TrafficMatrix TrafficMatrixSequence::getMatrix(unsigned int index) const {
	if(index >= this->sequence.size())
		throw IndexOutOfBoundsException(index);

	return this->sequence[index];
}

} //namespace