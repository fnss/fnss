/**
 * TOPOLOGY EXAMPLE
 * ================
 *
 * This example shows how to parse a topology from an XML file, list all nodes
 * and edges and get all attributes of nodes, edges, stacks and applications.
 */
#include "topology.h"
#include "edge.h"
#include "pair.h"
#include "parser.h"

#include <exception>
#include <iostream>
#include <set>
#include <sstream>

using namespace std;

/**
 * Return a stream with all properties of the container
 */
string listProperties(const fnss::PropertyContainer &p) {
	ostringstream ss;

	set<string> s = p.getAllProperties();
	for(set<string>::iterator it = s.begin(); it != s.end(); it++)
		ss<<*it<<" = "<<p.getProperty(*it)<<endl;

	return ss.str();
}

/**
 * Return a stream with all applications of the node and their properties
 */
string listApplications(const fnss::Node &n) {
	ostringstream ss;	

	set<string> s = n.getAllApplications();
	for(set<string>::iterator it = s.begin(); it != s.end(); it++)
		ss<< n.getApplication(*it).getName()<<":"<<endl
			<<listProperties(n.getApplication(*it));

	return ss.str();
}

/**
 * Return a stream with properties of the edge
 */
string listEdge(const fnss::Edge &e) {
	ostringstream ss;

	ss<<"Capacity: "<<e.getCapacity().toString()<<"	Delay: "<<e.getDelay().toString()
		<<"	Weight: "<<e.getWeight()<<"	BufferSize: "<<e.getBufferSize().toString()<<endl;

	return ss.str();
}


int main(int argc, char* argv[]) {
	if (argc != 2) {
		cerr<<"Usage: example topology_file.xml"<<endl;
		exit(1);
	}

	// Import topology from file
	fnss::Topology topology = fnss::Parser::parseTopology(argv[1]);

	// get all information about the topology to print on screen
	ostringstream ss;

	// get list of all edges
	set<pair <string, string> > edges = topology.getAllEdges();

	// get list of all nodes
	set<string> nodes = topology.getAllNodes();

	ss<<"*** TOPOLOGY EXAMPLE ***"<<endl<<endl;

	ss<<"*** SUMMARY ***"<<endl;
	// get topology type (directed or undirected)
	ss<<"Directed:	"<<(topology.isDirected() ? "true" : "false")<<endl;
	// get node and edge count
	ss<<"Node count:	"<<topology.nodeCount()<<endl;
	ss<<"Edge count:	"<<topology.edgeCount()<<endl;

	ss<<endl;

	ss<<"*** NODES ***"<<endl;

	// iterates through all nodes
	for(set<string>::iterator it = nodes.begin(); it != nodes.end(); it++) {
		ss<<"[NODE "<<*it<<"]"<<endl;
		// get all properties of a node
		ss<<"Properties: "<<endl<<listProperties(topology.getNode(*it));

		// get the name of the stack
		ss<<"Stack: "<<topology.getNode(*it).getProtocolStack().getName()<<endl;

		// list all properties of the stack
		ss<<listProperties(topology.getNode(*it).getProtocolStack());

		// list all applications on the node and their properties
		ss<<"Applications: "<<endl<<listApplications(topology.getNode(*it))<<endl;
	}

	// iterate through all edges and print all edge properties
	ss<<endl<<"*** EDGES ***"<<endl;
	for(set<pair <string, string> >::iterator it = edges.begin(); it != edges.end(); it++)

		// Print on screen edge and properties
		ss<<"[EDGE "<<(*it).first<<"->"<<(*it).second<<"] "<<listEdge(topology.getEdge(*it));

	// Print everything on screen
	cout<<ss.str()<<endl;

	return 0;
}
