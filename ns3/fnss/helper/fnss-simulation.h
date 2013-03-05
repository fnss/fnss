#ifndef FNSS_SIMULATION_H
#define FNSS_SIMULATION_H
	
#include "ns3/topology.h"
#include "ns3/event-schedule.h"
#include "ns3/fnss-event.h"

#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/point-to-point-module.h"

#include <string>
#include <map>
#include <list>

namespace ns3 {

/**
 * Helps with setting up a FNSS-based simulation.
 */
class FNSSSimulation {
public:
	/**
	 * Create the simulation from a XML topology file.
	 *
	 * @param file the XML topology file to parse.
	 */
	FNSSSimulation(const std::string &file);

	/**
	 * Create the simulation from a fnss::Topology object.
	 *
	 * @param the fnss::Topology object to use.
	 */
	FNSSSimulation(const fnss::Topology &topology);

	/**
	 * Create events from a XML event schedule file.
	 * Every event must have a event_type property that must match an existing
	 * class name deriving from ns3::FNSSEvent.
	 *
	 * @param file the XML event schedule file to parse.
	 */
	void scheduleEvents(const std::string &file);
	
	/**
	 * Create events from a fnss::EventSchedule object.
	 * Every event must have a event_type property that must match an existing
	 * class name deriving from ns3::FNSSEvent.
	 *
	 * @param schedule the fnss::EventSchedule object to use.
	 */
	void scheduleEvents(const fnss::EventSchedule &schedule);

	/**
	 * Assign ipv4 addresses to the crated links, one /30 subnet per link.
	 * 
	 * @param base the address base.
	 */
	void assignIPv4Addresses(const Ipv4Address &base = Ipv4Address("10.0.0.0"));

	/**
	 * Get a reference to the ns3::PointToPointHelper that was used when creating
	 * the links. Useful for enabling PCAP capture form the main simulation.
	 *
	 * @return reference to the helper object.
	 */
	PointToPointHelper& getP2PHHelper();

	/**
	 * Get a ns3::Ptr to the specified node.
	 *
	 * @param id the id of the requested node.
	 * @return a Ptr<Node> to the requested node object.
	 */
	Ptr<Node> getNode(const std::string &id) const;

	/**
	 * Get a std::list of ns3::NetDeviceContainers. Each NetDeviceContainer has two
	 * elements, the end points of a link.
	 *
	 * @return the set of NetDeviceContainers.
	 */
	std::list<NetDeviceContainer> getAllEdgeDevices() const;

	/**
	 * Get a std::map from application name to ns3::Application pointer of all the
	 * applications installed on the specified node.
	 *
	 * @param id the id of the node.
	 * @return the application map.
	 */
	std::map <std::string, Ptr <Application> > getApplications(const std::string &id) const;

private:
	void applyProperties(Ptr <Object> target, const fnss::PropertyContainer &properties);

	void buildTopology(const fnss::Topology &topology);

	void doEvents(const fnss::EventSchedule &schedule);

	typedef struct {
		Ptr <Node> m_ptr;
		std::map <std::string, Ptr <Application> > m_applications;
	} NodesValue;

	typedef std::map<std::string, NodesValue> NodesMap;
	NodesMap m_nodes;

	std::list<NetDeviceContainer> m_links;

	PointToPointHelper m_p2p;

	std::list<Ptr<EventImpl> > track;
	std::list<Ptr<FNSSEvent> > track2;
};
}

#endif //FNSS_SIMULATION_H