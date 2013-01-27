#include "property-container.h"

namespace fnss {

std::string PropertyContainer::getProperty(const std::string &name) const {
	propertiesType::const_iterator it;
	it = this->properties.find(name);

	if(it != this->properties.end())
		return it->second;
	else
		throw PropertyNotFoundException(name);
}

// std::string PropertyContainer::getProperty(const std::string &name,
// 										bool &found) const {
// 	propertiesType::const_iterator it;
// 	it = this->properties.find(name);
// 	if(it != this->properties.end()) {
// 		found = true;
// 		return it->second;
// 	}
// 	else {
// 		found = false;
// 		return std::string("");
// 	}
// }

void PropertyContainer::setProperty(const std::string &name,
								const std::string &value) {
	this->properties[name] = value;
}

bool PropertyContainer::hasProperty(const std::string &name) const {
	propertiesType::const_iterator it = this->properties.find(name);

	if(it == this->properties.end())
		return false;
	else
		return true;
}

void PropertyContainer::addProperties(const PropertyContainer &other) {
	propertiesType::const_iterator it;
	for(it = other.properties.begin(); it != other.properties.end(); it++)
		this->properties[it->first] = it->second;
}

std::string PropertyContainer::removeProperty(const std::string &name) {
	propertiesType::iterator it;
	it = this->properties.find(name);

	if(it != this->properties.end()) {
		std::string ret = it->second;
		this->properties.erase(it);
		return ret;
	} else
		throw PropertyNotFoundException(name);
}

// std::string PropertyContainer::removeProperty(const std::string &name,
// 												bool &found) {
// 	propertiesType::iterator it;
// 	it = this->properties.find(name);
//
// 	if(it != this->properties.end()) {
// 		found = true;
// 		std::string ret = it->second;
// 		this->properties.erase(it);
// 		return ret;
// 	} else {
// 		found = false;
// 		return std::string("");
// 	}
// }

std::set<std::string> PropertyContainer::getAllProperties() const {
	std::set<std::string> keys;
	propertiesType::const_iterator it;
	for(it = this->properties.begin(); it != this->properties.end(); it++)
		keys.insert(it->first);
	return keys;
}

}
