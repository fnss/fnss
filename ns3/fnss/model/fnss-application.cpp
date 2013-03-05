#include "fnss-application.h"

namespace fnss {

Application::Application(const std::string &name) {
	this->name = name;
}

std::string Application::getName() const {
	return this->name;
}

void Application::setName(const std::string &name) {
	this->name = name;
}

}