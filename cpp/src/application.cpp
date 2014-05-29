#include "application.h"

namespace fnss {

Application::Application(const std::string &name_) : name(name_) {}

std::string Application::getName() const {
	return this->name;
}

void Application::setName(const std::string &name_) {
	this->name = name_;
}

}