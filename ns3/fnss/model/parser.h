#ifndef PARSER_H
#define PARSER_H

#include "topology.h"
#include "event-schedule.h"
#include "traffic-matrix-sequence.h"

#include <string>
#include "rapidxml.hpp"

namespace fnss {

/**
 * Static class containing XML parsing functionality.
 *
 * @author Cosmin Cocora
 */
class Parser {
public:
	/**
	 * Construct a \c Topology object by parsing an XML file.
	 * 
	 * @param file the XML file to parse.
	 * @return the constructed \c Topology object.
	 */
	static Topology parseTopology(const std::string &file);

	/**
	 * Construct a \c EventSchedule object by parsing an XML file.
	 * 
	 * @param file the XML file to parse.
	 * @return the constructed \c Topology object.
	 */
	static EventSchedule parseEventSchedule(const std::string &file);

	/**
	 * Construct a \c TrafficMatrixSequence object by parsing an XML file.
	 * 
	 * @param file the XML file to parse.
	 * @return the constructed \c Topology object.
	 */
	static TrafficMatrixSequence parseTrafficMatrixSequence(const std::string &file);

private:
	Parser();
	static PropertyContainer parseProperties(rapidxml::xml_node<>* node);
	static std::string getAttribute(rapidxml::xml_node<>* node,
									const std::string &name);
	static double AtoI(const std::string &value);
};


} //namespace

#endif //PARSER_H