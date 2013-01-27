#ifndef MEASUREMENT_UNIT_H
#define MEASUREMENT_UNIT_H

#include <map>
#include <set>
#include <string>

namespace fnss {

class MeasurementUnit {

public:
	/**
	 * Map from unit to the multiplier required to convert to the base unit,
	 * eg. km -> 1000.
	 */
	typedef std::map <std::string, double> conversionsMapType;

	/**
	 * Constructor.
	 *
	 * @param the base the unit base(eg. sec, m).
	 */
	MeasurementUnit(const std::string &base);

	/**
	 * Constructor.
	 *
	 * @param the base the unit base(eg. sec, m).
	 * @param the conversion map.
	 */
	MeasurementUnit(const std::string &base,
					const conversionsMapType &conversions);

	/**
	 * Convert the given unit to the base unit.
	 * Throws an exception if the conversion is not found in \c this->conversions.
	 *
	 * @return unit conversion multiplier.
	 */
	double convert(const std::string &unit) const;

	/**
	 * Convert between the given units.
	 * Throws an exception if the conversion is not found in \c this->conversions.
	 *
	 * @return the multiplier required to convert \c unit1 to \c unit2.
	 */
	double convert(const std::string &unit1, const std::string &unit2) const;

	/**
	 * Get the base unit.
	 *
	 * @return the base unit.
	 */
	std::string getBaseUnit() const;
	
	/**
	 * Get a \c std::set of all known units for this measure(eg. ms, us, mm).
	 *
	 * @return a \c std::set of all known units for this measure.
	 */
	std::set <std::string> getAllUnits() const;

	/**
	 * Add or overwrite a conversion unit.
	 *
	 * @param unit the unit the conversion if from.
	 * @param multiplier the multiplier of the conversion.
	 */
	void addConversion(std::string unit, double multiplier);

	/**
	 * Adds conversion unit. Does not overwrite exiting units.
	 *
	 * @param conversions \c conversionsMapType object to add.
	 */
	void addConversions(const conversionsMapType &conversions);

	/**
	 * Insert all the units from \c other into \c this. Does not overwrite
	 * existing units. Does not change \c this->base and \c other->base is just
	 * added to the conversions map.
	 * 
	 * @param  other the object to add the units from.
	 * @return       reference to \this for chaining.
	 */
	MeasurementUnit& combine(const MeasurementUnit &other);

	/**
	 * Assignment operator.
	 * Throws an exception if trying to assign an object with a different
	 * \c this->base.
	 */
	MeasurementUnit& operator=(const MeasurementUnit &other);
	
	/**
	 * Get an object with units constructed by applying all the units in the 
	 * \c prefix object to all the units in the \c target object.
	 *
	 * @param prefix the prefix unit.
	 * @param target the target unit.
	 */
	static MeasurementUnit prefixDerivation(const MeasurementUnit &prefix,
											const MeasurementUnit &target);

	/**
	 * Get an object with all the combinations of \c numerator over \c denominator
	 * units possible. The created unit string representation is "numerator + 
	 * separator + denominator".
	 * 
	 * @param  numerator   the numerator unit.
	 * @param  denominator the denominator unit.
	 * @param  separator   the separator used in the string representation.
	 * @return             the resulting unit.
	 */
	static MeasurementUnit fractionalDerivation(const MeasurementUnit &numerator,
												const MeasurementUnit &denominator,
												const std::string &separator);

	class UnknownConversionException : public std::exception {
	public:
		UnknownConversionException(const std::string &unit1,
									const std::string &unit2) throw() {
			this->exceptionStr = "Unknown conversion from unit " + unit1
								+ " to unit " + unit2 + ".";
		}

		~UnknownConversionException() throw() {
		}

		const char* what() const throw() {
			return this->exceptionStr.c_str();
		}

	private:
		std::string exceptionStr;
	};

	class BaseMismatchException : public std::exception {
	public:
		BaseMismatchException(const std::string &base1,
								const std::string &base2) throw() {
			this->exceptionStr = "Base unit mismatch: " + base1
								+ " and " + base2 + ".";
		}

		~BaseMismatchException() throw() {
		}

		const char* what() const throw() {
			return this->exceptionStr.c_str();
		}

	private:
		std::string exceptionStr;
	};

private:
	//Append the base unit to the \c conversions map, with a multiplier of 1.
	static conversionsMapType appendBase(const conversionsMapType &conversions,
										const std::string &base);


	const std::string base;	//Base unit this object operates with.

	//Map of all possible conversions to the base unit.
	conversionsMapType conversions;
};

} //namespace

#endif //MEASUREMENT_UNIT_H