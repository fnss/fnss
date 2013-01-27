#ifndef UNITS_H
#define UNITS_H

#define PACKET_SIZE 1500 * 8	//Conversion from packet to bit count for BufferSize.
#include "measurement-unit.h"

namespace fnss {

/**
 * Class containing some predefined measurement units.
 * 
 * WARNING: Data and bandwidth units use SI prefix, eg. 1kB = 1000 bytes, NOT 1024.
 *
 * @author Cosmin Cocora
 */
class Units {
public:
	static const MeasurementUnit SIPrefix;
	static const MeasurementUnit Time;
	static const MeasurementUnit Data;
	static const MeasurementUnit BufferSize;	//Appends "packet" unit to Data.
	static const MeasurementUnit Bandwidth;
	static const MeasurementUnit Distance;

private:
	Units();
};

} //namespace

#endif //UNITS_H
