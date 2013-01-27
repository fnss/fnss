#ifndef PROPERTY_CONTAINER_H
#define PROPERTY_CONTAINER_H

#include <string>
#include <map>
#include <set>

namespace fnss {

/**
 * Container class for <property_name, property_value> type data.
 *
 * @author Cosmin Cocora
 */
class PropertyContainer {
public:
	/**
	 * Get the value of the specified property.
	 * 
	 * Throws an exception if the specified property was not found.
	 * 
	 * @param  std::string name of the property.
	 * @return value of the property.
	 */
	std::string getProperty(const std::string &name) const;

	/**
	 * Get the value of the specified property.
	 * 
	 * @param  std::string name of the property.
	 * @param found set to \c true if the specified property was found, \c false
	 * otherwise
	 * @return value of the property (\c "" if not available).
	 */
	// std::string getProperty(const std::string &name, bool &found) const;

	/**
	 * Create or overwrite a property.
	 * 
	 * @param name  name of the property.
	 * @param value value of the property.
	 */
	void setProperty(const std::string &name, const std::string &value = "");

	/**
	 * Check whether the \c PropertyContainer has a specified property.
	 *
	 * @param name the name of the property to check.
	 */
	bool hasProperty(const std::string &name) const;

	/**
	 * Add or overwrite all the properties from a different \c PropertyContainer.
	 *
	 * @param other the object to copy the properties from.
	 */
	void addProperties(const PropertyContainer &other);

	/**
	 * Delete the specified property.
	 * 
	 * Throws an exception if the specified property was not found.
	 * 
	 * @param  name name of the property.
	 * @return value of the property.
	 */
	std::string removeProperty(const std::string &name);

	/**
	 * Delete the specified property.
	 * 
	 * @param  name name of the property.
	 * @param found set to \c true if the specified property was found, \c false
	 * otherwise.
	 * @return value of the property (\c "" if not available).
	 */
	// std::string removeProperty(const std::string &name, bool &found);

	/**
	 * Get all the property names in a set.
	 * 
	 * @return set containing all the property names.
	 */
	std::set<std::string> getAllProperties() const;

	class PropertyNotFoundException : public std::exception {
	public:
		PropertyNotFoundException(const std::string &name) throw() {
			this->exceptionStr = "The property named " + name + " was not found.";
		}

		~PropertyNotFoundException() throw() {
		}

		const char* what() const throw() {
			return this->exceptionStr.c_str();
		}

	private:
		std::string exceptionStr;
	};

private:
	/**
	 * Map from property name to property value
	 */
	typedef std::map <std::string, std::string> propertiesType;
	propertiesType properties;
};

} //namespace

#endif //PROPERTY_CONTAINER_H