#include "fnss-simulation.h"

#include <set>

#include "ns3/parser.h"
#include "ns3/node.h"
#include "ns3/fnss-node.h"
#include "ns3/fnss-event.h"
#include "ns3/quantity.h"

NS_LOG_COMPONENT_DEFINE ("FNSSSimulation");

namespace ns3 {

FNSSSimulation::FNSSSimulation(const fnss::Topology &topology) {
	this->buildTopology(topology);
}

FNSSSimulation::FNSSSimulation(const std::string &file) {
	fnss::Topology topology = fnss::Parser::parseTopology(file);
	this->buildTopology(topology);
}

void FNSSSimulation::scheduleEvents(const std::string &file) {
	fnss::EventSchedule schedule = fnss::Parser::parseEventSchedule(file);
	this->doEvents(schedule);
}

void FNSSSimulation::scheduleEvents(const fnss::EventSchedule &schedule) {
	this->doEvents(schedule);
}

PointToPointHelper& FNSSSimulation::getP2PHHelper() {
	return this->m_p2p;
}

Ptr<Node> FNSSSimulation::getNode(const std::string &id) const {
	NodesMap::const_iterator it = this->m_nodes.find(id);
	return it->second.m_ptr;
}

std::list<NetDeviceContainer> FNSSSimulation::getAllEdgeDevices() const {
	return this->m_links;
}

void FNSSSimulation::assignIPv4Addresses(const Ipv4Address &base) {
	Ipv4AddressHelper address;
	address.SetBase (base, "255.255.255.252");
	std::list<NetDeviceContainer>::iterator it = this->m_links.begin();
	while(it != this->m_links.end()) {
		address.Assign(*it);
		address.NewNetwork();
		it++;
	}
}

std::map <std::string, Ptr <Application> >  FNSSSimulation::getApplications(const std::string &id) const {
	NodesMap::const_iterator it = this->m_nodes.find(id);
	return it->second.m_applications;
}

void  FNSSSimulation::applyProperties(Ptr <Object> target, const fnss::PropertyContainer &properties) {
	std::set<std::string> names = properties.getAllProperties();

	for(std::set<std::string>::iterator it = names.begin(); it != names.end(); it++) {
		target->SetAttribute(*it, StringValue(properties.getProperty(*it)));
	}
}

void FNSSSimulation::buildTopology(const fnss::Topology &topology) {
	if(topology.isDirected()) {
		NS_LOG_ERROR("Directed topologies not supported.");
		return;
	}

	NS_LOG_INFO("Creating simulation from fnss::Topology object...");
	
	//Create the nodes.
	std::set<std::string> nodeIds = topology.getAllNodes();
	for(std::set<std::string>::iterator it = nodeIds.begin(); it != nodeIds.end(); it++) {
		NodesValue val;
		val.m_ptr = CreateObject <Node>();
		this->m_nodes[*it] = val;
	}
	NS_LOG_INFO("Created " << this->m_nodes.size() <<" nodes.");

	//Create the links.
	std::set<std::pair < std::string, std::string > > edges = topology.getAllEdges();
	for(std::set<std::pair <std::string, std::string> >::iterator it = edges.begin();
		it != edges.end(); it++) {

		fnss::Edge edge = topology.getEdge(*it);

		//Set the edge attributes.
		this->m_p2p.SetDeviceAttribute("DataRate", StringValue(edge.getCapacity().toString()));
		this->m_p2p.SetChannelAttribute("Delay", StringValue(edge.getDelay().toString()));

		NetDeviceContainer p2pDev;
		p2pDev.Add(this->m_p2p.Install(this->m_nodes[(*it).first].m_ptr,
										this->m_nodes[(*it).second].m_ptr));
		this->m_links.push_back(p2pDev);
	}
	NS_LOG_INFO("Created " << this->m_links.size() <<" edges.");

	//Install the default internet stack on all nodes.
	InternetStackHelper internet;
	for(NodesMap::iterator it = this->m_nodes.begin(); it != this->m_nodes.end(); it++) {
		internet.Install(it->second.m_ptr);
	}
	NS_LOG_INFO("Installed the default Internet stack on all nodes.");

	//Install applications on nodes.
	ObjectFactory factory;
	for(std::set<std::string>::iterator it = nodeIds.begin(); it != nodeIds.end(); it++) {
		fnss::Node node = topology.getNode(*it);
		std::set<std::string> applications = node.getAllApplications();

		for(std::set<std::string>::iterator appIt = applications.begin();
			appIt != applications.end(); appIt++) {

			factory.SetTypeId (*appIt);
			Ptr<Application> app = factory.Create <Application>();
			this->applyProperties(app, node.getApplication(*appIt));

			this->m_nodes[*it].m_ptr->AddApplication(app);
			this->m_nodes[*it].m_applications[*appIt] = app;
		}
	}
}

void FNSSSimulation::doEvents(const fnss::EventSchedule &schedule) {
	ObjectFactory factory;

	for(uint32_t i = 0; i < schedule.size(); i++) {
		fnss::Event e = schedule.getEvent(i);

		//Create the event.
		e.removeProperty("event_type");
		Ptr<FNSSEvent> fnssEvent = CreateObject <FNSSEvent> ();
  		this->applyProperties(fnssEvent, e);

  		//Schedule the event.
  		Ptr<EventImpl> downcastEvent = DynamicCast <EventImpl, FNSSEvent> (fnssEvent);
  		fnss::Quantity t = e.getTime();
  		t.convert("ms");
  		std::string str = t.toString();
  		str.erase(remove_if(str.begin(), str.end(), isspace), str.end());
  		Simulator::Schedule(Time(str), downcastEvent);
	}

	NS_LOG_INFO("Scheduled events.");
}

} //namespace