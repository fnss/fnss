#include "protocol-stack.h"

namespace fnss {

ProtocolStack::ProtocolStack(const std::string &name_) : name(name_) {}

std::string ProtocolStack::getName() const {
	return this->name;
}

void ProtocolStack::setName(const std::string &name_) {
	this->name = name_;
}

}