#include "traffic-matrix.h"

#include "units.h"

namespace fnss {

unsigned int TrafficMatrix::size() const {
	return this->matrix.size();
}

Quantity TrafficMatrix::getFlow(const std::string &source,
								const std::string &destination) const {
	return this->getFlow(std::pair<std::string, std::string>(source, destination));
}

Quantity TrafficMatrix::getFlow(const std::pair<std::string, std::string> &nodes) const {
	matrixType::const_iterator it = this->matrix.find(nodes);

	if(it == this->matrix.end())
		return Quantity(0, Units::Bandwidth);
	return it->second;
}

void TrafficMatrix::setFlow(const std::string &source,
							const std::string &destination,
							const Quantity &volume) {
	this->setFlow(std::pair<std::string, std::string>(source, destination), volume);
}

void TrafficMatrix::setFlow(const std::pair<std::string, std::string> &nodes,
							const Quantity &volume) {
	matrixType::iterator it = this->matrix.find(nodes);

	if(it != this->matrix.end())
		this->matrix.erase(it);	//Avoid using operator[].

	if(volume > Quantity(0, Units::Bandwidth))
		this->matrix.insert(std::make_pair(nodes, volume));
}

std::set<std::pair<std::string, std::string> > TrafficMatrix::getPairs() const {
	std::set<std::pair<std::string, std::string> > pairs;
	matrixType::const_iterator it;

	for(it = this->matrix.begin(); it != this->matrix.end(); it++)
		pairs.insert(it->first);

	return pairs;
}

}