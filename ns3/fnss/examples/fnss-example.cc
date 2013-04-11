/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

#include "ns3/core-module.h"
#include "ns3/fnss-simulation.h"
#include "ns3/udp-echo-client.h"
#include "ns3/fnss-event.h"

#include <string>
#include <iostream>

using namespace ns3;

int main (int argc, char *argv[])
{
	std::string topologyFile = "src/fnss/examples/res/topology.xml";
	std::string eventsFile = "src/fnss/examples/res/eventschedule.xml";
 
	LogComponentEnable("FNSSSimulation", LOG_LEVEL_INFO);
	LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
	LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO);
	LogComponentEnable("FNSSEvent", LOG_LEVEL_INFO);

	FNSSSimulation sim(topologyFile);
	sim.assignIPv4Addresses();
	sim.scheduleEvents(eventsFile);

	Simulator::Run ();
	Simulator::Destroy ();
	return 0;
}


