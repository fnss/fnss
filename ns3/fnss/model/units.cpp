#include "units.h"

#include <math.h>

namespace fnss {

MeasurementUnit initSIPrefix() {
	MeasurementUnit::conversionsMapType map;

	map[""] = 1;
	map["T"] = pow((double) 10, (double) 12);
	map["G"] = pow((double) 10, (double) 9);
	map["M"] = pow((double) 10, (double) 6);
	map["k"] = pow((double) 10, (double) 3);
	map["d"] = pow((double) 10, (double) -1);
	map["n"] = pow((double) 10, (double) -9);
	map["c"] = pow((double) 10, (double) -2);
	map["m"] = pow((double) 10, (double) -3);
	map["u"] = pow((double) 10, (double) -6);

	return MeasurementUnit("", map);
}

MeasurementUnit initTime() {
	MeasurementUnit t("s");	//Time base is s.

	//Add prefixes before other units.
	t =  MeasurementUnit::prefixDerivation(Units::SIPrefix, t);

	//Add other units.
	MeasurementUnit::conversionsMapType map;
	map["sec"] = 1;
	map["second"] = map["sec"];
	map["seconds"] = map["sec"];

	map["min"] = map["sec"] * 60;
	map["minute"] = map["min"];
	map["minutes"] = map["min"];
	map["m"] = map["min"];

	map["hour"] = map["min"] * 60;
	map["hours"] = map["hour"];
	map["h"] = map["hour"];

	map["day"] = map["hour"] * 24;
	map["days"] = map["day"];
	map["d"] = map["day"];

	map["week"] = map["day"] * 7;
	map["weeks"] = map["week"];

	t.addConversions(map);
	return t;
}

MeasurementUnit initData() {
	MeasurementUnit d("b");
	d.addConversion("B", 8);
	return MeasurementUnit::prefixDerivation(Units::SIPrefix, d);
}

MeasurementUnit initBufferSize() {
	MeasurementUnit b = Units::Data;
	b.addConversion("packets", PACKET_SIZE);
	return b;
}

MeasurementUnit initBandwidth() {
	MeasurementUnit B1 = MeasurementUnit::fractionalDerivation(Units::Data,
												Units::Time, "/");
	MeasurementUnit B2 = MeasurementUnit::fractionalDerivation(Units::Data,
												Units::Time, "p");

	return B1.combine(B2);
}

MeasurementUnit initDistace() {
	MeasurementUnit d("m");
	return MeasurementUnit::prefixDerivation(Units::SIPrefix, d);
}

const MeasurementUnit Units::SIPrefix = initSIPrefix();
const MeasurementUnit Units::Time = initTime();
const MeasurementUnit Units::Data = initData();
const MeasurementUnit Units::BufferSize = initBufferSize();
const MeasurementUnit Units::Bandwidth = initBandwidth();
const MeasurementUnit Units::Distance = initDistace();

} //namespace
