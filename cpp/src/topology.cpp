#include "topology.h"

#include <queue>

namespace fnss {

Topology::Topology(bool directed_) : directed(directed_) {}

bool Topology::isDirected() const {
	return this->directed;
}

void Topology::addNode(const std::string &id, const Node &node) {
	this->nodes[id] = node;
}

Node Topology::removeNode(const std::string &id, bool pruneEdges) {
	nodesType::iterator it_nodes = this->nodes.find(id);
	if(it_nodes == this->nodes.end())
		throw NodeNotFoundException(id);

	Node ret = it_nodes->second;
	this->nodes.erase(it_nodes);

	if(pruneEdges) {
		std::queue<edgesType::iterator> eraseQueue;
		edgesType::iterator it;
		for(it = this->edges.begin(); it != this->edges.end(); it++) {
			if(it->first.first == id || it->first.second == id)
				eraseQueue.push(it);
		}

		while(! eraseQueue.empty()) {
			this->edges.erase(eraseQueue.front());
			eraseQueue.pop();
		}
	}

	return ret;
}

Node Topology::getNode(const std::string &id) const {
	nodesType::const_iterator it = this->nodes.find(id);
	if(it == this->nodes.end())
		throw NodeNotFoundException(id);

	return it->second;
}

bool Topology::hasNode(const std::string &id) const {
	nodesType::const_iterator it = this->nodes.find(id);
	if(it == this->nodes.end())
		return false;
	else
		return true;
}

std::set<std::string> Topology::getAllNodes() const {
	std::set<std::string> nodeIds;

	nodesType::const_iterator it;
	for(it = this->nodes.begin(); it != this->nodes.end(); it++)
		nodeIds.insert(it->first);

	return nodeIds;
}

void Topology::addEdge(const std::string &id1, const std::string &id2, const Edge &edge) {
	this->addEdge(Pair<std::string, std::string>(id1, id2), edge);
}

void Topology::addEdge(const Pair <std::string, std::string> &nodes_, const Edge &edge) {
	if(! this->hasNode(nodes_.first))
		throw NodeNotFoundException(nodes_.first);
	else if(! this->hasNode(nodes_.second))
		throw NodeNotFoundException(nodes_.second);

	//Create a fnss::Pair that is commutative if the topology is not directed
	Pair<std::string, std::string> key(nodes_);
	key.setCommutative(! this->directed);

	this->edges[key] = edge;
}

void Topology::addEdge(const std::pair <std::string, std::string> &nodes_, const Edge &edge) {
	this->addEdge(Pair<std::string, std::string>(nodes_), edge);
}

Edge Topology::removeEdge(const Pair <std::string, std::string> &nodes_) {
	edgesType::iterator it = this->edges.find(nodes_);

	if(it == this->edges.end())
		throw EdgeNotFoundException(nodes_);

	Edge ret = it->second;
	this->edges.erase(it);
	return ret;
}

Edge Topology::removeEdge(const std::pair <std::string, std::string> &nodes_) {
	return this->removeEdge(Pair<std::string, std::string>(nodes_));
}

Edge Topology::removeEdge(const std::string &id1, const std::string &id2) {
	return this->removeEdge(Pair<std::string, std::string>(id1, id2));
}

Edge Topology::getEdge(const Pair <std::string, std::string> &nodes_) const {
	edgesType::const_iterator it = this->edges.find(nodes_);

	if(it == this->edges.end())
		throw EdgeNotFoundException(nodes_);

	return it->second;
}

Edge Topology::getEdge(const std::pair <std::string, std::string> &nodes_) const {
	return this->getEdge(Pair<std::string, std::string>(nodes_));
}

Edge Topology::getEdge(const std::string &id1, const std::string &id2) const {
	return this->getEdge(Pair<std::string, std::string>(id1, id2));
}

bool Topology::hasEdge(const Pair <std::string, std::string> &nodes_) const {
	edgesType::const_iterator it = this->edges.find(nodes_);

	if(it == this->edges.end())
		return false;
	else
		return true;
}

bool Topology::hasEdge(const std::pair <std::string, std::string> &nodes_) const {
	return this->hasEdge(Pair<std::string, std::string>(nodes_));
}

bool Topology::hasEdge(const std::string &id1, const std::string &id2) const {
	return this->hasEdge(Pair<std::string, std::string>(id1, id2));
}

std::set <std::pair <std::string, std::string> > Topology::getAllEdges() const {
	std::set <std::pair <std::string, std::string> > edgeSet;

	edgesType::const_iterator it;
	for(it = this->edges.begin(); it != this->edges.end(); it++)
		edgeSet.insert(it->first.getStlPair());

	return edgeSet;
}

unsigned int Topology::nodeCount() const {
	return this->nodes.size();
}

unsigned int Topology::edgeCount() const {
	return this->edges.size();
}
} //namespace
