#include "measurement-unit.h"

namespace fnss {

MeasurementUnit::MeasurementUnit(const std::string &base) : base(base) {
	this->conversions[base] = 1;
}

MeasurementUnit::MeasurementUnit(const std::string &base,
								const conversionsMapType &conversions) :
									base(base), 
									conversions(appendBase(conversions, base)) {
}

double MeasurementUnit::convert(const std::string &unit) const {
	conversionsMapType::const_iterator it = this->conversions.find(unit);
	
	if(it == this->conversions.end())
		throw UnknownConversionException(unit, this->base);
	return it->second;
}

double MeasurementUnit::convert(const std::string &unit1,
								const std::string &unit2) const {
	conversionsMapType::const_iterator it1 = this->conversions.find(unit1);
	conversionsMapType::const_iterator it2 = this->conversions.find(unit2);

	if(it1 == this->conversions.end())
		throw UnknownConversionException(unit1, this->base);
	else if(it2 == this->conversions.end())
		throw UnknownConversionException(unit2, this->base);
	return it1->second * (1 / it2->second);
}

std::string MeasurementUnit::getBaseUnit() const {
	return this->base;
}

std::set <std::string> MeasurementUnit::getAllUnits() const {
	std::set <std::string> ret;

	conversionsMapType::const_iterator it;
	for(it = this->conversions.begin();	it != this->conversions.end(); it++)
		ret.insert(it->first);

	return ret;
}

void MeasurementUnit::addConversion(std::string unit, double multiplier) {
	this->conversions[unit] = multiplier;
}

void MeasurementUnit::addConversions(const conversionsMapType &conversions) {
	this->conversions.insert(conversions.begin(), conversions.end());
}

MeasurementUnit& MeasurementUnit::combine(const MeasurementUnit &other) {
	this->conversions.insert(other.conversions.begin(), other.conversions.end());

	return *this;
}

MeasurementUnit& MeasurementUnit::operator=(const MeasurementUnit &other) {
	if(this->base != other.base)
		throw BaseMismatchException(this->base, other.base);
	
	this->conversions = other.conversions;	//std::map operator= checks for
											//self-assignment.

	return *this;
}

MeasurementUnit MeasurementUnit::prefixDerivation(const MeasurementUnit &prefix,
												const MeasurementUnit & target) {
	conversionsMapType map;
	std::string base = prefix.getBaseUnit() + target.getBaseUnit();

	std::set <std::string> prefixUnits = prefix.getAllUnits();
	std::set <std::string> targetUnits = target.getAllUnits();
	std::set <std::string>::iterator prefixIt, targetIt;

	for(targetIt = targetUnits.begin(); targetIt != targetUnits.end(); targetIt++)
		for(prefixIt = prefixUnits.begin(); prefixIt != prefixUnits.end(); prefixIt++)
			map[*prefixIt + *targetIt] = prefix.convert(*prefixIt) *
											target.convert(*targetIt);

	return MeasurementUnit(base, map);
}

MeasurementUnit MeasurementUnit::fractionalDerivation(const MeasurementUnit &numerator,
													const MeasurementUnit &denominator,
													const std::string &separator) {
	conversionsMapType map;
	std::string base = numerator.getBaseUnit() + separator + denominator.getBaseUnit();

	std::set <std::string> numeratorUnits = numerator.getAllUnits();
	std::set <std::string> denominatorUnits = denominator.getAllUnits();
	std::set <std::string>::iterator numeratorIt, denominatorIt;

	for(numeratorIt = numeratorUnits.begin(); numeratorIt != numeratorUnits.end();
		numeratorIt++)
		for(denominatorIt = denominatorUnits.begin();
			denominatorIt != denominatorUnits.end(); denominatorIt++)
			map[*numeratorIt + separator + *denominatorIt] =
				numerator.convert(*numeratorIt) / denominator.convert(*denominatorIt);

	return MeasurementUnit(base, map);
}

MeasurementUnit::conversionsMapType MeasurementUnit::appendBase(
								const conversionsMapType &conversions,
								const std::string &base) {
	conversionsMapType map(conversions);
	map[base] = 1;
	return map;
}
}