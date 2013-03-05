#include "fnss-node.h"

namespace fnss {

Node::Node(const ProtocolStack &stack) : stack(stack) {

}

ProtocolStack Node::getProtocolStack() const {
	return this->stack;
}

void Node::setProtocolStack(const ProtocolStack &stack) {
	this->stack = stack;
}

Application Node::getApplication(const std::string &name) const {
	ApplicationsType::const_iterator it;
	it = this->applications.find(name);

	if(it != this->applications.end()) 
		return Application(it->second);
	else
		throw ApplicationNotFoundException(name);
}

// Application Node::getApplication(const std::string &name, bool &found) const {
// 	ApplicationsType::const_iterator it;
// 	it = this->Applications.find(name);
//
// 	if(it != this->Applications.end()) {
// 		found = true;
// 		return Application(it->second);
// 	}
// 	else {
// 		found = false;
// 		return Application();
// 	}
// }

void Node::setApplication(const Application &application) {
	this->applications[application.getName()] = application;
}

Application Node::removeApplication(const std::string &name) {
	ApplicationsType::iterator it;
	it = this->applications.find(name);

	if(it != this->applications.end()) {
		Application ret = it->second;
		this->applications.erase(it);
		return ret;
	} else
		throw ApplicationNotFoundException(name);
}

// Application Node::removeApplication(const std::string &name, bool &found) {
// 	ApplicationsType::iterator it;
// 	it = this->Applications.find(name);

// 	if(it != this->Applications.end()) {
// 		found = true;
// 		Application ret = it->second;
// 		this->Applications.erase(it);
// 		return ret;
// 	} else {
// 		found = false;
// 		return Application();
// 	}
// }

std::set <std::string> Node::getAllApplications() const {
	std::set<std::string> keys;
	ApplicationsType::const_iterator it;
	for(it = this->applications.begin();it != this->applications.end(); it++)
		keys.insert(it->first);
	return keys;
}

}
