#ifndef EDGE_H
#define EDGE_H

#include "quantity.h"
#include "units.h"

#include <string>

namespace fnss {

/**
 * Default link capacity, set if no capacity is specified in the constructor
 */
#define DEFAULT_CAPACITY "1Mbps"

/**
 * Default link delay, set if no delay is specified in the constructor
 */
#define DEFAULT_DELAY "1ms"

/**
 * Default link weight, set if no link weight is specified in the constructor
 */
#define DEFAULT_WEIGHT 1

/**
 * Default buffer size, set if no buffer size is specified in the constructor
 */
#define DEFAULT_BUFFER_SIZE "100packets"

/**
 * Represent an edge of a topology
 *
 * @author Cosmin Cocora
 */
class Edge {
public:
	/**
	 * Constructor.
	 */
	Edge(const Quantity &capacity_ = Quantity(DEFAULT_CAPACITY, Units::Bandwidth),
		const Quantity &delay_ = Quantity(DEFAULT_DELAY, Units::Time),
		const float &weight_ = DEFAULT_WEIGHT,
		const Quantity &bufferSize_ = Quantity(DEFAULT_BUFFER_SIZE, Units::BufferSize));

	/**
	 * Get the capacity of the link.
	 *
	 * @return the capacity.
	 */
	Quantity getCapacity() const;

	/**
	 * Set the the link's capacity.
	 *
	 * @param capacity the link's capacity.
	 */
	void setCapacity(const Quantity &capacity_);

	/**
	 * Get the weight of the link.
	 *
	 * @return the weight of the link.
	 */
	float getWeight() const;

	/**
	 * Set the weight of the link.
	 *
	 * @param weight the weight of the link.
	 */
	void setWeight(float weight_);

	/**
	 * Get the delay of the link.
	 *
	 * @return the delay of the link.
	 */
	Quantity getDelay() const;

	/**
	 * Set the the link's delay.
	 *
	 * @param delay the link's delay.
	 */
	void setDelay(const Quantity &delay_);

	/**
	 * Get the size of the buffer associated with this link.
	 *
	 * @return the buffer's size.
	 */
	Quantity getBufferSize() const;

	/**
	 * Set the size of the buffer associated with this link.
	 *
	 * @param bufferSize the buffer's size.
	 */
	void setBufferSize(const Quantity &bufferSize_);

private:
	Quantity capacity;
	float weight;
	Quantity delay;
	Quantity bufferSize;
};

} //namespace

#endif //EDGE_H
