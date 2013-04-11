#include "quantity.h"

#include <sstream>

namespace fnss {

Quantity::Quantity(const double &value, const std::string &unit,
					const MeasurementUnit &converter) : converter(converter) {
	this->value = value;
	this->unit = unit;
}

Quantity::Quantity(const double &value, const MeasurementUnit &converter) :
														converter(converter) {
	this->value = value;
	this->unit = converter.getBaseUnit();
}

Quantity::Quantity(const std::string &str, const MeasurementUnit &converter) :
														converter(converter) {
	this->fromString(str);
}

Quantity::Quantity(const MeasurementUnit &converter) : converter(converter) {
	this->value = 0;
	this->unit = converter.getBaseUnit();
}

void Quantity::fromString(const std::string &str) {
	std::istringstream ss(str);
	ss>>this->value>>this->unit;

	if(this->unit == "")
		this->unit = this->converter.getBaseUnit();
}

std::string Quantity::toString(const std::string &separator) const {
	std::ostringstream ss;
	ss<<this->value;
	return ss.str() + separator + this->unit;
}

void Quantity::convert(const std::string &unit) {
	this->value *= this->converter.convert(this->unit, unit);
	this->unit = unit;
}

double Quantity::getValue() const {
	return this->value;
}

void Quantity::setValue(const double &value) {
	this->value = value;
}

std::string Quantity::getUnit() const {
	return this->unit;
}

void Quantity::setUnit(const std::string &unit) {
	this->unit = unit;
}

const MeasurementUnit& Quantity::getMeasurementUnit() const {
	return this->converter;
}

Quantity& Quantity::operator=(const Quantity &other) {
	if(this->converter.getBaseUnit() != other.getMeasurementUnit().getBaseUnit())
		throw MeasurementUnit::BaseMismatchException(this->converter.getBaseUnit(),
										other.getMeasurementUnit().getBaseUnit());
	this->value = other.value;
	this->unit = other.unit;

	return *this;
}

bool Quantity::operator<(const Quantity &other) const {
	return this->value * this->converter.convert(this->unit) <
			other.value * this->converter.convert(other.unit);
}

bool Quantity::operator<=(const Quantity &other) const {
	return this->value * this->converter.convert(this->unit) <=
			other.value * this->converter.convert(other.unit);
}

bool Quantity::operator>(const Quantity &other) const {
	return this->value * this->converter.convert(this->unit) >
			other.value * this->converter.convert(other.unit);
}

bool Quantity::operator>=(const Quantity &other) const {
	return this->value * this->converter.convert(this->unit) >=
			other.value * this->converter.convert(other.unit);
}

bool Quantity::operator==(const Quantity &other) const {
	return this->value * this->converter.convert(this->unit) ==
			other.value * this->converter.convert(other.unit);
}

} //namespace
