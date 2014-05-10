#include <functional>
#include <exception>
#include <iostream>
#include <set>
#include <sstream>
#include <math.h>

#include "event.h"
#include "event-schedule.h"
#include "measurement-unit.h"
#include "units.h"
#include "quantity.h"
#include "topology.h"
#include "edge.h"
#include "pair.h"
#include "traffic-matrix.h"
#include "traffic-matrix-sequence.h"
#include "parser.h"

using namespace std;
using namespace fnss;

string removeWS(const string &str) {
	istringstream ss(str);
	string ret;
	while(ss>>ret);
	return ret;
}

string listProperties(const PropertyContainer &p) {
	ostringstream ss;

	set<string> s = p.getAllProperties();
	for(set<string>::iterator it = s.begin(); it != s.end(); it++)
		ss<<*it<<" = "<<p.getProperty(*it)<<endl;

	return ss.str();
}

string listApplications(const Node &n) {
	ostringstream ss;

	set<string> s = n.getAllApplications();
	for(set<string>::iterator it = s.begin(); it != s.end(); it++)
		ss<< n.getApplication(*it).getName()<<":"<<endl
			<<listProperties(n.getApplication(*it));

	return ss.str();
}

string listEdge(const Edge &e) {
	ostringstream ss;

	ss<<"Capacity: "<<e.getCapacity().toString()<<"	Delay: "<<e.getDelay().toString()
		<<"	Weight: "<<e.getWeight()<<"	BufferSize: "<<e.getBufferSize().toString()<<endl;

	return ss.str();
}

string listEventSchedule(const EventSchedule &es) {
	ostringstream ss;

	unsigned int s = es.size();
	ss<<"Start time: "<<es.getStartTime().toString()<<endl;
	ss<<"End time: "<<es.getEndTime().toString()<<endl;
	ss<<"Event count: "<<s<<endl;

	for(unsigned int i = 0; i < s; i++) {
		Event e = es.getEvent(i);
		ss<<"Event "<<i<<" (time "<<e.getTime().toString()<<"):"<<endl;
		ss<<listProperties(e);
	}

	return ss.str();
}

string listTrafficMatrix(const TrafficMatrix &m) {
	ostringstream ss;

	ss<<"Flow count: "<<m.size()<<endl;

	set<pair<string, string> > s = m.getPairs();
	set<pair<string, string> >::iterator it = s.begin();
	for(; it != s.end(); it++)
		ss<<(*it).first<<"->"<<(*it).second<<": "<<m.getFlow(*it).toString()<<endl;

	return ss.str();
}

string listTrafficMatrixSequence(const TrafficMatrixSequence &s) {
	ostringstream ss;

	ss<<"Matrix count: "<<s.size()<<endl;
	ss<<"Time interval: "<<s.getInterval().toString()<<endl;

	for(unsigned int i = 0; i < s.size(); i++) {
		TrafficMatrix m = s.getMatrix(i);
		ss<<"Matrix "<<i<<":"<<endl<<listTrafficMatrix(m);
	}

	return ss.str();
}

string listNodes(const Topology &t) {
	ostringstream ss;

	set<string> nodes = t.getAllNodes();

	ss<<"Nodes:"<<endl;
	for(set<string>::iterator it = nodes.begin(); it != nodes.end(); it++)
		ss<<"  Node "<<*it<<":"<<endl
			<<"    properties: "<<endl<<listProperties(t.getNode(*it))<<endl
			<<"    stack: "<<t.getNode(*it).getProtocolStack().getName()<<endl
			<<listProperties(t.getNode(*it).getProtocolStack())
			<<"    applications:"<<endl<<listApplications(t.getNode(*it))<<endl;

	return ss.str();
}

string listEdges(const Topology &t) {
	ostringstream ss;

	set<pair <string, string> > edges = t.getAllEdges();

	ss<<"  Edges:"<<endl;
	for(set<pair <string, string> >::iterator it = edges.begin();
		it != edges.end(); it++)
		ss<<"    Edge "<<(*it).first<<"->"<<(*it).second<<":"<<listEdge(t.getEdge(*it));

	return ss.str();
}

string listTopology(const Topology &t) {
	ostringstream ss;

	ss<<"Directed:	"<<(t.isDirected() ? "true" : "false")<<endl;
	ss<<"Node count:	"<<t.nodeCount()<<endl;
	ss<<"Edge count:	"<<t.edgeCount()<<endl;

	ss << listNodes(t) << listEdges(t);

	return ss.str();
}

void listUnits(const MeasurementUnit &unit) {
	cout<<"Units with base "<<unit.getBaseUnit()<<":"<<endl;

	set <string> units = unit.getAllUnits();
	set <string>::iterator it1, it2;

	for(it1 = units.begin(); it1 != units.end(); it1++)
		cout<<"	"<<*it1<<"	: "<<unit.convert(*it1)<<endl;

	for(it1 = units.begin(); it1 != units.end(); it1++)
		for(it2 = units.begin(); it2 != units.end(); it2++)
			cout<<"	"<<*it1<<"->"<<*it2<<"	: "<<unit.convert(*it1, *it2)<<endl;
}

void testPair() {
	cout<<"Pair test: ";
	Pair <string, string> p1;
	Pair <string, string> p2("str1", "str2");
	Pair <string, string> p3(p2.getStlPair());
	pair<string, string> stlPair("str3", "str4");
	Pair <string, string> p4(stlPair, true);
	p1 = p2;

	assert(p1.getCommutative() == false);
	assert(p2.getCommutative() == false);
	assert(p3.getCommutative() == false);
	assert(p4.getCommutative() == true);
	assert(p1 == p2);
	assert(p2 == p3);

	p3.second="str3";
	assert(p2 != p3);

	p3.first="str4";
	assert(p3 == p4);

	cout<<"passed"<<endl;
}

void testTopology(bool directed = false) {
	string linkType = directed ? "directed" : "undirected";
	cout<<"Topology test, "<<linkType<<" links: ";

	Topology t = Topology(directed);
	assert(t.isDirected() == directed);

	ProtocolStack p1("stack1"), p2("stack2"), p3("stack3");
	p1.setProperty("stack prop 1", "test 1");
	p2.setProperty("stack prop 2", "test 2");
	p3.setProperty("stack prop 3", "test 3");

	Edge e1, e2;
	e1.setCapacity(Quantity("50kb/s", Units::Bandwidth));

	Application a1, a2("app2");
	a1.setName("app1");

	Node n1, n2, n3(p3), n4;
	n1.setProtocolStack(p1);
	n2.setProtocolStack(p2);
	n1.setApplication(a1);
	n1.setApplication(a2);
	n2.setApplication(a1);
	n3.setApplication(a2);

	t.addNode("Node 1", n1);
	t.addNode("Node 2", n2);
	t.addNode("Node 3", n3);
	t.addNode("Node 4", n4);
	assert(t.nodeCount() == 4);

	t.addEdge("Node 1", "Node 2", e1);
	t.addEdge("Node 2", "Node 1", e2);
	assert(t.hasEdge("Node 1", "Node 2"));
	assert(t.hasEdge("Node 2", "Node 1"));

	if (t.isDirected()) {
		assert(t.edgeCount() == 2);
		assert(t.getEdge("Node 1", "Node 2").getCapacity() == e1.getCapacity());
	} else {
		assert(t.edgeCount() == 1);
		assert(t.getEdge("Node 1", "Node 2").getCapacity() == e2.getCapacity());
	}
	// cout<<listTopology(t);
	t.addEdge("Node 2", "Node 3", e2);
	t.addEdge("Node 1", "Node 4", e1);

	//TODO: This test case fails with undirected topology only:
	assert(t.hasEdge("Node 2", "Node 1"));

	assert(t.hasEdge("Node 1", "Node 4"));
	if(!t.isDirected()) {
		assert(t.hasEdge("Node 4", "Node 1"));
	}

	t.addNode("Node 5", n4);
	t.addEdge(pair<string, string>("Node 4", "Node 5"), e2);
	assert(t.hasEdge("Node 4", "Node 5"));
	assert(t.hasEdge(pair<string, string>("Node 4", "Node 5")));
	if(!t.isDirected()) {
		assert(t.hasEdge("Node 5", "Node 4"));
		assert(t.hasEdge(pair<string, string>("Node 5", "Node 4")));
	}

	t.removeNode("Node 1");
	assert(t.nodeCount() == 4);
	assert(!t.hasEdge("Node 1", "Node 2"));

	bool except = false;
	try {
		t.removeEdge("Node 5", "Node 6");
	} catch (exception &e) {
		except = true;
	}
	assert(except);
	except = false;
	try {
		t.getEdge("Node 8", "Node 9");
	} catch (exception &e) {
		except = true;
	}
	assert(except);

	cout<<"passed"<<endl;
}

void testNode(Node n = Node()) {
	cout<<"Node test: ";

	Application a1("app1"), a2("app2");
	a1.setProperty("application 1 property 1", "test 1");
	a1.setProperty("application 1 property 2", "test 2");
	a2.setProperty("application 2 property 1", "test 3");
	a2.setProperty("application 2 property 2", "test 4");

	n.setApplication(a1);
	n.setApplication(a2);
	set<string> allApps = n.getAllApplications();
	assert(allApps.find("app1") != allApps.end());
	assert(allApps.find("app2") != allApps.end());
	assert(allApps.size() == 2);
	n.removeApplication("app1");
	assert(n.getAllApplications().size() == 1);
	n.removeApplication("app2");
	assert(n.getAllApplications().size() == 0);

	bool except = false;
	try {
		n.removeApplication("N/A");
	} catch(exception &e) {
		except = true;
	}
	assert(except);
	cout<<"passed"<<endl;
}

void testEdge() {
	cout<<"Edge test: ";

	Edge e;
	// test default values
	assert(e.getCapacity().toString() == "1Mbps");
	assert(e.getDelay().toString() == "1ms");
	assert(e.getWeight() == 0);
	assert(e.getBufferSize().toString() == "10packets");

	e.setCapacity(Quantity("5kb/s", Units::Bandwidth));
	e.setDelay(Quantity("0.5s", Units::Time));
	e.setWeight(2);
	e.setBufferSize(Quantity("1kB", Units::Data));

	assert(e.getCapacity().toString() == "5kb/s");
	assert(e.getDelay().toString() == "0.5s");
	assert(e.getWeight() == 2);
	assert(e.getBufferSize().toString() == "1kB");

	cout<<"passed"<<endl;
}

void testPropertyContainer(PropertyContainer p = PropertyContainer()) {
	cout<<"PropertyContainer test: ";

	assert(p.getAllProperties().size() == 0);

	p.setProperty("test1", "test1 value");
	p.setProperty("test2", "test2 value");
	p.setProperty("test3", "test3 value");

	assert(p.hasProperty("test1"));
	assert(p.hasProperty("test2"));
	assert(p.hasProperty("test3"));
	assert(p.getProperty("test1") == "test1 value");
	assert(p.getProperty("test2") == "test2 value");
	assert(p.getProperty("test3") == "test3 value");
	assert(p.getAllProperties().size() == 3);

	p.removeProperty("test2");
	assert(!p.hasProperty("test2"));
	assert(p.getAllProperties().size() == 2);

	bool except = false;
	try {
		p.removeProperty("N/A");
	} catch(exception &e) {
		except = true;
	}
	assert(except);
	except = false;
	try {
		p.getProperty("Not there");
	} catch(exception &e) {
		except = true;
	}
	assert(except);

	cout<<"passed"<<endl;
}

void testProtocolStack(ProtocolStack p = ProtocolStack("test protocol stack")) {
	cout<<"ProtocolStack test: ";

	assert(p.getName() == "test protocol stack");
	p.setName("changed name");
	assert(p.getName() == "changed name");

	cout<<"passed"<<endl;
}

void testTrafficMatrix(TrafficMatrix m = TrafficMatrix()) {
	cout<<"TrafficMatrix test: ";

	m.setFlow("node1", "node2", Quantity("1Gb/s", Units::Bandwidth));
	assert(m.size() == 1);

	assert(m.getFlow("node1", "node2") == Quantity("1Gbps", Units::Bandwidth));
	pair<string, string> p("node2", "node1");
	m.setFlow(p, Quantity("0.1Gb/s", Units::Bandwidth));
	assert(m.getFlow("node2", "node1") == Quantity("0.1Gbps", Units::Bandwidth));
	assert(m.getFlow("node1", "node2") == Quantity("1Gbps", Units::Bandwidth));
	assert(m.size() == 2);

	m.setFlow(p, Quantity("0GB/s", Units::Bandwidth));
	assert(m.size() == 1);

	assert(m.getFlow("N/A", "N/A") == Quantity("0GB/s", Units::Bandwidth));

	cout<<"passed"<<endl;
}

void testTrafficMatrixSequence(TrafficMatrixSequence s = TrafficMatrixSequence()) {
	cout<<"TrafficMatrixSequence test: ";

	s.setInterval(Quantity("2s", Units::Time));
	assert(s.getInterval() == Quantity("2s", Units::Time));

	TrafficMatrix m;
	assert(s.size() == 0);

	m.setFlow("node1", "node2", Quantity("1Gbps", Units::Bandwidth));
	s.addMatrix(m, 3);
	assert(s.size() == 4);
	assert(s.getMatrix(3).getFlow("node1", "node2") == Quantity("1Gbps", Units::Bandwidth));

	m.setFlow("node1", "node2", Quantity("2Gbps", Units::Bandwidth));
	s.addMatrix(m, 1);
	assert(s.size() == 4);
	assert(s.getMatrix(3).getFlow("node1", "node2") == Quantity("1Gbps", Units::Bandwidth));
	assert(s.getMatrix(1).getFlow("node1", "node2") == Quantity("2Gbps", Units::Bandwidth));

	m.setFlow("node1", "node2", Quantity("3Gbps", Units::Bandwidth));
	s.addMatrix(m);
	assert(s.size() == 5);
	assert(s.getMatrix(3).getFlow("node1", "node2") == Quantity("1Gbps", Units::Bandwidth));
	assert(s.getMatrix(1).getFlow("node1", "node2") == Quantity("2Gbps", Units::Bandwidth));
	assert(s.getMatrix(4).getFlow("node1", "node2") == Quantity("3Gbps", Units::Bandwidth));

	s.removeMatrix(4);
	assert(s.size() == 4);

	s.removeMatrix(2);
	assert(s.size() == 4);

	s.addMatrix(m, 4);
	assert(s.size() == 5);

	bool except = false;
	try {
		s.removeMatrix(8);
	} catch(exception &e) {
		except = true;
	}
	assert(except);
	except = false;
	try {
		s.getMatrix(5);
	} catch(exception &e) {
		except = true;
	}
	assert(except);
	cout<<"passed"<<endl;
}

void testEventSchedule(EventSchedule es = EventSchedule()) {
	cout<<"EventSchedule test: ";

	Event e1, e2, e3;
	e1.setTime(Quantity("10min", Units::Time));
	e2.setTime(Quantity("2h", Units::Time));
	e3.setTime(Quantity("110min", Units::Time));

	es.setStartTime(Quantity("10s", Units::Time));
	es.setEndTime(Quantity("3h", Units::Time));
	assert(es.getStartTime() == Quantity("10s", Units::Time));
	assert(es.getEndTime() == Quantity("3h", Units::Time));

	assert(es.size() == 0);

	es.addEvent(e1);
	assert(es.size() == 1);

	es.addEvent(e2);
	assert(es.size() == 2);
	assert(es.getEvent(0).getTime() == e1.getTime());
	assert(es.getEvent(1).getTime() == e2.getTime());

	es.addEvent(e3);
	assert(es.size() == 3);
	assert(es.getEvent(0).getTime() == e1.getTime());
	assert(es.getEvent(1).getTime() == e3.getTime());
	assert(es.getEvent(2).getTime() == e2.getTime());

	es.removeEvent(1);
	assert(es.size() == 2);
	assert(es.getEvent(1).getTime() == e2.getTime());

	bool except = true;
	try {
		es.getEvent(5);
	} catch(exception &e) {
		except = true;
	}
	assert(except);
	except = false;
	try {
		es.removeEvent(4);
	} catch(exception &e) {
		except = true;
	}
	assert(except);

	cout<<"passed"<<endl;
}

void testEvent() {
	cout<<"Event test: ";

	// default event time = 0s
	Event e1, e2(Quantity("1min", Units::Time));
	e1.setProperty("key 1.1", "val 1.1");
	e1.setProperty("key 1.2", "val 1.2");
	e2.setProperty("key 2.1", "val 2.1");
	e2.setProperty("key 2.2", "val 2.2");
	assert(e1.getAllProperties().size() == 2);
	assert(e2.getAllProperties().size() == 2);
	assert(e1.getProperty("key 1.1") == "val 1.1");
	assert(e1.getProperty("key 1.2") == "val 1.2");
	assert(e2.getProperty("key 2.1") == "val 2.1");
	assert(e2.getProperty("key 2.2") == "val 2.2");

	assert(e2 > e1);
	e1.setTime(Quantity("61sec", Units::Time));
	assert(e2 < e1);

	cout<<"passed"<<endl;
}

void testQuantity() {
	cout<<"Quantity test: ";
	Quantity t1(Units::Time);
	Quantity t2(1, "h", Units::Time);
	Quantity t3("60min", Units::Time);
	Quantity t4("3601 sec", Units::Time);
	t1.fromString("2days");
	assert(t2 == t3);
	assert(t4 > t2);

	t1.convert("h");
	t2.convert("h");
	t3.convert("h");
	t4.convert("h");
	assert(t1.toString() == "48h");
	assert(t2.toString() == "1h");
	assert(t3.toString() == "1h");

	// test default
	assert(Quantity(Units::Time) == Quantity("0s", Units::Time));

	// test buffer size conversion (default MTU = 1500B)
	Quantity buffSize("2 packets", Units::BufferSize);
	buffSize.convert("B");
	assert(buffSize.toString() == "3000B");

	// attempt mismatched unit conversion (time -> bandwidth)
	bool except = false;
	try {
		t1.convert("MB");
	} catch(exception &e) {
		except = true;
	}
	assert(except);
	except = false;
	try {
		t1 = Quantity(Units::Data);
	} catch(exception &e) {
		except = true;
	}
	assert(except);

	cout<<"passed"<<endl;
}

void testUnits() {
	cout<<"Test Units: ";

	MeasurementUnit dist = MeasurementUnit(Units::Bandwidth);
	assert(dist.getBaseUnit() == "b/s");
	assert(dist.convert("kbps") == 1000);

	cout<<"passed"<<endl;
}

void testParser() {
	cout<<"Parser test: ";

	Topology t = Parser::parseTopology("res/topology.xml");
	assert(!t.isDirected());
	assert(t.getAllNodes().size() == 10);
	assert(t.getAllEdges().size() == 18);
	assert(t.getNode("2").getProperty("longitude") == "99.76");

	EventSchedule es = Parser::parseEventSchedule("res/eventschedule.xml");
	assert(es.getStartTime() == Quantity("1s", Units::Time));
	assert(es.getEndTime() == Quantity("1m", Units::Time));
	assert(es.size() == 3);
	assert(es.getEvent(1).getProperty("content_id") == "146");

	TrafficMatrixSequence tms = Parser::parseTrafficMatrixSequence("res/tm.xml");
	assert(tms.size() == 3);
	assert(tms.getMatrix(1).getFlow("LA", "2") == Quantity("9876340.002Mbps", Units::Bandwidth));

	cout<<"passed"<<endl;
}

int main() {
	testPair();
	testTopology(true);
	testTopology(false);
	testNode();
	testEdge();
	testPropertyContainer();
	testProtocolStack();
	testTrafficMatrix();
	testTrafficMatrixSequence();
	testEventSchedule();
	testEvent();
	testQuantity();
	testUnits();
	testParser();
	return 0;
}
