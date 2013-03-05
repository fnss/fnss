#include "parser.h"

#include <fstream>
#include <sstream>
#include <iostream>

namespace fnss {

Topology Parser::parseTopology(const std::string &file) {

	std::ifstream fin(file.c_str());
	std::ostringstream sstr;
	sstr << fin.rdbuf();
	
	sstr.flush();
	fin.close();
	
	std::string xmlData = sstr.str();
	rapidxml::xml_document<> doc;
	doc.parse<0> (&xmlData[0]);
	
	rapidxml::xml_node<> *rootNode = doc.first_node("topology");
	rapidxml::xml_node<> *curNode;

	if(!rootNode)
		return Topology();
 	
 	std::string directedStr = Parser::getAttribute(rootNode, "linkdefault");
 	bool directed = false;
 	if(directedStr == "directed")
 		directed = true;
	Topology t(directed);
 	
 	PropertyContainer topologyProperties = Parser::parseProperties(rootNode);
 	std::string capacityUnit = topologyProperties.getProperty("capacity_unit");
 	std::string delayUnit = topologyProperties.getProperty("delay_unit");
 	std::string bufferUnit = topologyProperties.getProperty("buffer_unit");

 	curNode = rootNode->first_node("node");
 	while(curNode) {
 		Node n;
 		std::string id = Parser::getAttribute(curNode, "id");
 		
 		PropertyContainer nodeProperties = Parser::parseProperties(curNode);
 		n.addProperties(nodeProperties);
 		
 		rapidxml::xml_node<> *aux = curNode->first_node("stack");
 		ProtocolStack stack;
 		std::string stackName;
 		PropertyContainer stackProperties;
 		if(aux) {
 			stackProperties = Parser::parseProperties(aux);
 			stackName = Parser::getAttribute(aux, "name");
 		}
 		stack.setName(stackName);
 		stack.addProperties(stackProperties);
 		n.setProtocolStack(stack);

 		aux = curNode->first_node("application");
 		while(aux) {
 			Application app;
 			PropertyContainer appProperties = Parser::parseProperties(aux);
 			app.setName(Parser::getAttribute(aux, "name"));
 			app.addProperties(appProperties);
 			n.setApplication(app);

 			aux = aux->next_sibling("application");
 		}

 		t.addNode(id, n);

 		curNode = curNode->next_sibling("node");
 	}

 	curNode = rootNode->first_node("link");
	while(curNode) {
		std::string to = curNode->first_node("to")->value();
		std::string from = curNode->first_node("from")->value();
		
		Edge edge;
		PropertyContainer edgeProperties = Parser::parseProperties(curNode);
		if(edgeProperties.hasProperty("delay"))
			edge.setDelay(Quantity(AtoI(edgeProperties.getProperty("delay")), 
						delayUnit, Units::Time));
		if(edgeProperties.hasProperty("capacity"))
			edge.setCapacity(Quantity(AtoI(edgeProperties.getProperty("capacity")), 
						capacityUnit, Units::Bandwidth));
		if(edgeProperties.hasProperty("buffer_size"))
			edge.setBufferSize(Quantity(AtoI(edgeProperties.getProperty("buffer_size")), 
						bufferUnit, Units::BufferSize));

		t.addEdge(from, to, edge);

		curNode = curNode->next_sibling("link");
	}

	return t;
}

EventSchedule Parser::parseEventSchedule(const std::string &file) {

	std::ifstream fin(file.c_str());
	std::ostringstream sstr;
	sstr << fin.rdbuf();
	
	sstr.flush();
	fin.close();
	
	std::string xmlData = sstr.str();
	rapidxml::xml_document<> doc;
	doc.parse<0> (&xmlData[0]);
	
	rapidxml::xml_node<> *rootNode = doc.first_node("event-schedule");
	rapidxml::xml_node<> *curNode;

	EventSchedule es;

	if(!rootNode)
		return es;

	PropertyContainer eventScheduleProperties = Parser::parseProperties(rootNode);
	std::string timeUnit;
	if(eventScheduleProperties.hasProperty("t_unit")) {
		timeUnit = eventScheduleProperties.getProperty("t_unit");
		if(eventScheduleProperties.hasProperty("t_start"))
			es.setStartTime(Quantity(AtoI(eventScheduleProperties.getProperty("t_start")),
									timeUnit, Units::Time));
		if(eventScheduleProperties.hasProperty("t_end"))
			es.setEndTime(Quantity(AtoI(eventScheduleProperties.getProperty("t_end")),
									timeUnit, Units::Time));
	}

	curNode = rootNode->first_node("event");
	while(curNode) {
		std::string time = Parser::getAttribute(curNode, "time");
		PropertyContainer eventProperties = Parser::parseProperties(curNode);
		
		Event e;
		if(time != "")
			e.setTime(Quantity(AtoI(time), timeUnit, Units::Time));
		e.addProperties(eventProperties);

		es.addEvent(e);

		curNode = curNode->next_sibling("event");
	}

	return es;
}

TrafficMatrixSequence Parser::parseTrafficMatrixSequence(const std::string &file) {
	TrafficMatrixSequence tms;

	std::ifstream fin(file.c_str());
	std::ostringstream sstr;
	sstr << fin.rdbuf();
	
	sstr.flush();
	fin.close();
	
	std::string xmlData = sstr.str();
	rapidxml::xml_document<> doc;
	doc.parse<0> (&xmlData[0]);
	
	rapidxml::xml_node<> *rootNode = doc.first_node("traffic-matrix");
	rapidxml::xml_node<> *curNode;

	if(!rootNode)
		return tms;

	PropertyContainer tmsProperties = Parser::parseProperties(rootNode);
	Quantity interval(Units::Time);
	if(tmsProperties.hasProperty("t_unit") && tmsProperties.hasProperty("interval")) {
		std::string timeUnit = tmsProperties.getProperty("t_unit");
		std::string intervalStr = tmsProperties.getProperty("interval");
		interval = Quantity(AtoI(intervalStr), timeUnit, Units::Time);
	}
	tms.setInterval(interval);

	curNode = rootNode->first_node("time");
	while(curNode) {
		std::string seqStr = Parser::getAttribute(curNode, "seq");
		unsigned int seq = 0;
		if(seqStr != "")
			seq = AtoI(seqStr);
		PropertyContainer mProperties = Parser::parseProperties(curNode);
		std::string volumeUnit;
		if(mProperties.hasProperty("volume_unit"))
			volumeUnit = mProperties.getProperty("volume_unit");
		TrafficMatrix m;

		rapidxml::xml_node<> *aux = curNode->first_node("origin");
		while(aux) {
			std::string origin = Parser::getAttribute(aux, "id");
			
			rapidxml::xml_node<> *aux2 = aux->first_node("destination");
			while(aux2) {
				std::string destination = Parser::getAttribute(aux2, "id");

				Quantity volume(AtoI(aux2->value()), volumeUnit, Units::Bandwidth);
				m.setFlow(origin, destination, volume);

				aux2 = aux2->next_sibling("destination");
			}

			aux = aux->next_sibling("origin");
		}

		tms.addMatrix(m, seq);

		curNode = curNode->next_sibling("time");
	}

	return tms;
}

PropertyContainer Parser::parseProperties(rapidxml::xml_node<>* node) {
	PropertyContainer p;
	rapidxml::xml_node<>* curNode = node->first_node("property");

	while(curNode) {
		std::string name = Parser::getAttribute(curNode, "name");
		if(name != "")
			p.setProperty(name, curNode->value());
		curNode = curNode->next_sibling("property");
	}

	return p;
}

std::string Parser::getAttribute(rapidxml::xml_node<>* node,
								const std::string &name) {
	rapidxml::xml_attribute<> *attr = node->first_attribute(name.c_str());
	if(attr)
		return attr->value();
	else
		return std::string();
}

double Parser::AtoI(const std::string &value) {
	double ret;
	std::istringstream ss(value);
	ss>>ret;
	return ret;
}

} //namespace