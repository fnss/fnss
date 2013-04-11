#ifndef QUANTITY_H
#define QUANTITY_H

#include "measurement-unit.h"

#include <string>

namespace fnss {

/**
 * Models a quantity and allows for conversions between measurement units of the
 * same type.
 *
 * @author Cosmin Cocora.
 */
class Quantity {
public:
	/**
	 * Constructor with explicit numerical value and unit.
	 *
	 * @param value the numeric value of the quantity.
	 * @param unit the value of the quantity's unit.
	 * @param converter the \c MeasurementUnit object used for conversions. The
	 *                  object is not copied, only the reference is stored.
	 */
	Quantity(const double &value, const std::string &unit,
				const MeasurementUnit &converter);

	/**
	 * Constructor with explicit numerical value.
	 * 
	 * The unit is assigned to the base of \c this->converter.
	 * Mainly declared to avoid calls of the type
	 * Quantity(0, someUnit) that would otherwise match the string constructor.
	 *
	 * @param value the numeric value of the quantity.
	 * @param converter the \c MeasurementUnit object used for conversions. The
	 *                  object is not copied, only the reference is stored.
	 */
	Quantity(const double &value, const MeasurementUnit &converter);

	/**
	 * Constructor that parses a string to obtain the numerical value and unit.
	 * 
	 * If not provided in the input, the unit is assumed to be the base of
	 * \c this->converter.
	 *
	 * @param str the \c std::string to be parsed for value and unit data.
	 * @param converter the \c MeasurementUnit object used for conversions. The
	 *                  object is not copied, only the reference is stored.
	 */
	Quantity(const std::string &str, const MeasurementUnit &converter);

	/**
	 * Constructor.
	 *
	 * @param converter the \c MeasurementUnit object used for conversions. The
	 *                  object is not copied, only the reference is stored.
	 */
	Quantity(const MeasurementUnit &converter);

	/**
	 * Parse a string to obtain the numerical value and unit. The previously stored
	 * data is discarded.
	 * 
	 * @param str the \c std::string to be parsed for value and unit data.
	 */
	void fromString(const std::string &str);

	/**
	 * Obtain a string representation of the object(eg. "5 GB/s").
	 * 
	 * If not provided in the input, the unit is assumed to be the base of
	 * \c this->converter.
	 *
	 * @param separator the \c std::the separator to insert between value and unit.
	 *
	 * @return the \c std::string representation of the object.
	 */
	std::string toString(const std::string &separator="") const;

	/**
	 * Convert to the specified unit(eg. from GB/s to Tb/h).
	 *
	 * @param unit the unit to convert to.
	 */
	void convert(const std::string &unit);

	/**
	 * Get method for the numerical value of the quantity.
	 *
	 * @return the numerical value of the quantity.
	 */
	double getValue() const;

	/**
	 * Set method for the numerical value of the quantity.
	 *
	 * @param value the numerical value to set.
	 */
	void setValue(const double &value);

	/**
	 * Get method for the unit of the quantity.
	 *
	 * @return the unit of the quantity.
	 */
	std::string getUnit() const;

	/**
	 * Set method for the unit of the quantity.
	 *
	 * @param unit the unit to set.
	 */
	void setUnit(const std::string &unit);

	/**
	 * Get a \c const reference to the \c MeasurementUnit object that \this is
	 * using for conversions.
	 *
	 * @return the \c const reference to the \c MeasurementUnit object being used. 
	 */
	const MeasurementUnit& getMeasurementUnit() const;

	/**
	 * Assignment operator.
	 * 
	 * Throws an exception if the \c MeasurementUnit reference
	 * of the \c other object has a different base from the \c MeasurementUnit
	 * reference of \this.
	 */
	Quantity& operator=(const Quantity &other);

	/**
	 * Comparison operator that takes into account the quantity's measurement unit.
	 */
	bool operator<(const Quantity &other) const;

	/**
	 * Comparison operator that takes into account the quantity's measurement unit.
	 */
	bool operator<=(const Quantity &other) const;

	/**
	 * Comparison operator that takes into account the quantity's measurement unit.
	 */
	bool operator>(const Quantity &other) const;

	/**
	 * Comparison operator that takes into account the quantity's measurement unit.
	 */
	 bool operator>=(const Quantity &other) const;

	 /**
	 * Comparison operator that takes into account the quantity's measurement unit.
	 */
	bool operator==(const Quantity &other) const;

private:
	double value;	//The numerical value of the quantity.
	std::string unit;	//The measurement unit of the quantity.
	const MeasurementUnit &converter;	//The "type" of the unit, used for
										//comparisons and conversions.
};

} //namespace

#endif //QUANTITY_H
