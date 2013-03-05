#include "protocol-stack.h"

namespace fnss {

ProtocolStack::ProtocolStack(const std::string &name) {
	this->name = name;
}

std::string ProtocolStack::getName() const {
	return this->name;
}

void ProtocolStack::setName(const std::string &name) {
	this->name = name;
}

}