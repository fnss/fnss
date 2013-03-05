#ifndef TRAFFIC_MATRIX_H
#define TRAFFIC_MATRIX_H

#include "quantity.h"

#include <string>
#include <set>
#include <map>
#include <utility>

namespace fnss {

/**
 * Represent a traffic matrix (referring to a single time interval.
 * 
 * @author Lorenzo Saino
 *
 */
class TrafficMatrix {
public:
/**
 * Get the number of flows in the matrix.
 *
 * @return the number of flows in the matrix.
 */
unsigned int size() const;

/**
 * Get the traffic volume between the specified nodes.
 * 
 * Returns \c Quantity(0,Units::Data) if the flow is not defined.
 *
 * @param source the source node of the flow.
 * @param destination the destination node of the flow.
 * @return the traffic volume.
 */
Quantity getFlow(const std::string &source, const std::string &destination) const;

/**
 * Get the traffic volume between the specified node pair.
 * 
 * Returns \c Quantity(0,Units::Data) if the flow is not defined.
 *
 * @param nodes the pair of <source, destination> nodes.
 * @return the traffic volume.
 */
Quantity getFlow(const std::pair<std::string, std::string> &nodes) const;

/**
 * Set the traffic volume between the specified nodes.
 *
 * @param source the source node of the flow.
 * @param destination the destination node of the flow.
 * @param volume the traffic volume.
 */
void setFlow(const std::string &source, const std::string &destination,
				const Quantity &volume);

/**
 * Set the traffic volume between the specified node pair.
 *
 * @param nodes the pair of <source, destination> nodes.
 * @param volume the traffic volume.
 */
void setFlow(const std::pair<std::string, std::string> &nodes, const Quantity &volume);

/**
 * Get all the existing flows as <source, destination> pairs.
 * 
 * Will only return flows of non-zero volume,
 *
 * @return all the <source, destination> pairs.
 */
std::set<std::pair<std::string, std::string> > getPairs() const;

private:
	/**
	 * Map from <Source, Destination> node pairs to traffic volume.
	 */
	typedef std::pair<std::string, std::string> matrixKeyType;
	typedef std::map<matrixKeyType, Quantity> matrixType;
	matrixType matrix;
};

} //namespace

#endif //TRAFFIC_MATRIX_H