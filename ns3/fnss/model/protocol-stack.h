#ifndef PROTOCOL_STACK_H
#define PROTOCOL_STACK_H

#include "property-container.h"

#include <string>

namespace fnss {

/**
 * Represent a protocol stack deployed on a node.
 * 
 * A protocol stack is identified by a name and contains a set of properties.
 * 
 * @author Cosmin Cocora
 *
 */
class ProtocolStack : public PropertyContainer {
public:
	/**
	 * Constructor.
	 * 
	 * @param name name of the protocol stack.
	 */
	ProtocolStack(const std::string &name = "");

	/**
	 * Get method for the protocol stack name.
	 *
	 * @return the name of the protocol stack.
	 */
	std::string getName() const;

	/**
	 * Set method for the protocol stack name.
	 * 
	 * @param name name of the protocol stack.
	 */
	void setName(const std::string &name);

private:
	/**
	 * Name of the protocol stack.
	 */
	std::string name;
};

} //namespace

#endif //PROTOCOL_STACK_H