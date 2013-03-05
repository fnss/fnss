#ifndef FNSS_NODE_H
#define FNSS_NODE_H

#include "property-container.h"
#include "protocol-stack.h"
#include "fnss-application.h"

#include <string>
#include <map>
#include <exception>

namespace fnss {

/**
 * Represent a node of a topology
 * 
 * Each node comprises a set of properties (e.g. if the node is a router/switch or host),
 * a protocol stack and multiple applications.
 *  
 * @author Cosmin Cocora
 */

class Node : public PropertyContainer {
public:
	/**
	 * Constructor.
	 *
	 * @param stack the \c ProtocolStack to be deployed on the node.
	 */
	Node(const ProtocolStack &stack = ProtocolStack());

	/**
	 * Get a copy of the \c ProtocolStack currently deployed on the node.
	 *
	 * @return the deployed \c ProtocolStack.
	 */
	ProtocolStack getProtocolStack() const;

	/**
	 * Overwrite the currently deployed \c ProtocolStack.
	 *
	 * @param stack the \c ProtocolStack to deploy.
	 */
	void setProtocolStack(const ProtocolStack &stack);

	/**
	 * Get a a copy of the application with the specified name.
	 * 
	 * Throws an exception if the specified application was not found.
	 * 
	 * @param name name of the application
	 * @return a copy of the \c Application object.
	 */
	Application getApplication(const std::string &name) const;

	/**
	 * Get a a copy of the application with the specified name.
	 * 
	 * @param name name of the application.
	 * @param found set to \c true if the \c Application with the specified
	 * name was found, \c false otherwise.
	 * @return a copy of the \c Application object if present or
	 * \c Application() otherwise.
	 */
	// Application getApplication(const std::string &name, bool &found) const;

	/**
	 * Deploy or overwrite the given \c Application on the node.
	 *
	 * @param application the \c Application to deploy.
	 */
	void setApplication(const Application &application);

	/**
	 * Remove the specified \c Application from the node.
	 * 
	 * Throws an exception if the specified application was not found.
	 *
	 * @param name name of the application to remove.
	 * @return a copy of the removed \c Application object.
	 */
	Application removeApplication(const std::string &name);

	/**
	 * Remove the specified \c Application from the node.
	 *
	 * @param name name of the application to remove.
	 * @param found set to \c true if the \c Application with the specified
	 * name was found, \c false otherwise.
	 * @return a copy of the \c Application object if present or
	 * \c Application() otherwise. 
	 */
	// Application removeApplication(const std::string &name, bool &found);

	/**
	 * Get a \c std::set containing the names of all the application
	 * deployed on the node.
	 *
	 * @return a set with all the names of the stacks deployed.
	 */
	std::set <std::string> getAllApplications() const;

	class ApplicationNotFoundException : public std::exception {
	public:
		ApplicationNotFoundException(const std::string &name) throw() {
			this->exceptionStr = "The application named " + name + " was not found.";
		}

		~ApplicationNotFoundException() throw() {
		}

		const char* what() const throw() {
			return this->exceptionStr.c_str();
		}

	private:
		std::string exceptionStr;
	};

private:
	/**
	 * Map from application name to application
	 */
	typedef std::map <std::string, Application> ApplicationsType;
	std::map <std::string, Application> applications;

	/**
	 * The protocol stack deployed on the node.
	 */
	ProtocolStack stack;
};

} //namespace

#endif	//FNSS_NODE_H