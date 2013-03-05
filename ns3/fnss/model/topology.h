#ifndef TOPOLOGY_H
#define TOPOLOGY_H

#include "property-container.h"
#include "ns3/fnss-node.h"
#include "edge.h"
#include "pair.h"

#include <map>
#include <set>
#include <utility>
#include <string>
#include <exception>

namespace fnss {

/**
 * Models a network topology.
 *
 * @author Cosmin Cocora
 */
class Topology : public PropertyContainer {
public:
	/**
	 * Constructor.
	 *
	 * @param directed whether the topology's edges are directed. For an undirected
	 * topology, all methods related to edges will treat the given node pairs as
	 * commutative(eg. removeEdge("node1", "node2") has the same effect as
	 * removeEdge("node2", "node2")).
	 */
	Topology(bool directed = false);

	/**
	 * Get method for the topology's edge type.
	 *
	 * @return \c true if the edges are directed, \c false otherwise.
	 */
	bool isDirected() const;

	/**
	 * Add a node to the topology.
	 * 
	 * If the ID of the node already exists it is overwritten.
	 *
	 * @param id the id of the node to be added.
	 * @param node the node object to add.
	 */
	void addNode(const std::string &id, const Node &node);

	/**
	 * Remove a node from the topology.
	 * 
	 * Also removes all the edges connected to the node unless explicitly told not to.
	 * Throws an exception if the given node id isn't found.
	 *
	 * @param id the id of the node to be removed.
	 * @param pruneEdges set to \c false to prevent the method from removing the
	 *                   edges connected to the erased node.
	 * @return a copy of the erased \c Node object.
	 */
	Node removeNode(const std::string &id, bool pruneEdges = true);

	/**
	 * Get a copy of the node with the specified id.
	 * 
	 * Throws an exception if the given node id isn't found.
	 *
	 * @param id the id of the requested node.
	 * @return a copy of the requested node.
	 */
	Node getNode(const std::string &id) const;

	/**
	 * Check whether the topology contains the node with the specified id.
	 * 
	 * @param  id the id of the node to lookup.
	 * @return    \c true if the node was found, \c false otherwise.
	 */
	bool hasNode(const std::string &id) const;

	/**
	 * Get a std::set<std::string> containing all the existing nodes' ids.
	 *
	 * @return a set containing the ids.
	 */
	std::set<std::string> getAllNodes() const;

	/**
	 * Add an edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge is created from the first specified
	 * node to the second.
	 * If one of the nodes doesn't exist, an exception is thrown.
	 *
	 * @param id1 the id of the first node.
	 * @param id2 the id of the second node.
	 * @param edge the \c Edge object.
	 */
	void addEdge(const std::string &id1, const std::string &id2, const Edge &edge);

	/**
	 * Add an edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge is created from the first node in
	 * the pair to the second.
	 * If one of the nodes doesn't exist, an exception is thrown.
	 *
	 * @param nodes the pair of nodes.
	 * @param edge the \c Edge object.
	 */
	void addEdge(const std::pair<std::string, std::string> &nodes, const Edge &edge);

	/**
	 * Add an edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge is created from the first node in
	 * the pair to the second.
	 * If one of the nodes doesn't exist, an exception is thrown.
	 *
	 * @param nodes the pair of nodes. The method ignores the commutativity
	 * property of the pair.
	 * @param edge the \c Edge object.
	 */
	void addEdge(const Pair<std::string, std::string> &nodes, const Edge &edge);

	/**
	 * Remove an edge from the topology.
	 * 
	 * If the topology is directed, the edge from the first specified node to
	 * the second is removed.
	 * Throws an exception if the edge is not found.
	 *
	 * @param id1 the id of the first node.
	 * @param id2 the id of the second node.
	 * @return a copy of the removed \c Edge object.
	 */
	Edge removeEdge(const std::string &id1, const std::string &id2);

	/**
	 * Remove an edge from the topology.
	 * 
	 * If the topology is directed, the edge from the first node in the pair to
	 * the second is removed.
	 * Throws an exception if the edge is not found.
	 *
	 * @param nodes the pair of nodes.
	 * @return a copy of the removed \c Edge object.
	 */
	Edge removeEdge(const std::pair <std::string, std::string> &nodes);

	/**
	 * Remove an edge from the topology.
	 * 
	 * If the topology is directed, the edge from the first node in the pair to
	 * the second is removed.
	 * Throws an exception if the edge is not found.
	 *
	 * @param nodes the pair of nodes. The method ignores the commutativity
	 * property of the pair.
	 * @return a copy of the removed \c Edge object.
	 */
	Edge removeEdge(const Pair <std::string, std::string> &nodes);

	/**
	 * Get a copy of the edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge from the first specified node to
	 * the second is returned.
	 * Throws an exception if the edge is not found.
	 *
	 * @param id1 the id of the first node.
	 * @param id2 the id of the second node.
	 * @retun a copy of the requested edge.
	 */
	Edge getEdge(const std::string &id1, const std::string &id2) const;

	/**
	 * Get a copy of the edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge from the first node in the pair 
	 * to the second is returned.
	 * Throws an exception if the edge is not found.
	 *
	 * @param nodes the pair of nodes.
	 * @retun a copy of the requested edge.
	 */
	Edge getEdge(const std::pair <std::string, std::string> &nodes) const;

	/**
	 * Get a copy of the edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge from the first node in the pair 
	 * to the second is returned.
	 * Throws an exception if the edge is not found.
	 *
	 * @param nodes the pair of nodes. The method ignores the commutativity
	 * property of the pair.
	 * @retun a copy of the requested edge.
	 */
	Edge getEdge(const Pair <std::string, std::string> &nodes) const;

	/**
	 * Check whether the topology contains an edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge from the first specified node to
	 * the second is checked.
	 *
	 * @param id1 the id of the first node.
	 * @param id2 the id of the second node.
	 * @return \c true if an edge exists, \c false otherwise.
	 */
	bool hasEdge(const std::string &id1, const std::string &id2) const;

	/**
	 * Check whether the topology contains an edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge from the first node in the pair to
	 * the second is checked.
	 *
	 * @param nodes the pair of nodes.
	 * @return \c true if an edge exists, \c false otherwise.
	 */
	bool hasEdge(const std::pair <std::string, std::string> &nodes) const;

	/**
	 * Check whether the topology contains an edge between the specified nodes.
	 * 
	 * If the topology is directed, the edge from the first node in the pair to
	 * the second is checked.
	 *
	 * @param nodes the pair of nodes. The method ignores the commutativity
	 * property of the pair.
	 * @return \c true if an edge exists, \c false otherwise.
	 */
	bool hasEdge(const Pair <std::string, std::string> &nodes) const;

	/**
	 * Get a \c std::set containing all the edges in the topology, represented
	 * as \c std::pairs containing the ids of the endpoints of each edge.
	 *
	 * @return a set with all edge endpoint pairs of the topology.
	 */
	std::set<std::pair <std::string, std::string> > getAllEdges() const;

	/**
	 * Get the number of nodes in the topology.
	 *
	 * @return the number of nodes.
	 */
	unsigned int nodeCount() const;

	/**
	 * Get the number of edges in the topology.
	 *
	 * @return the number of edges.
	 */
	unsigned int edgeCount() const;

	class EdgeNotFoundException : public std::exception {
	public:
		EdgeNotFoundException(const Pair<std::string, std::string> nodes) throw() {
			this->exceptionStr = "The edge between nodes with IDs " + nodes.first + " and "
								+ nodes.second + " was not found.";
		}

		~EdgeNotFoundException() throw() {
		}

		const char* what() const throw() {
			return this->exceptionStr.c_str();
		}

	private:
		std::string exceptionStr;
	};

	class NodeNotFoundException : public std::exception {
	public:
		NodeNotFoundException(const std::string &id) throw() {
			this->exceptionStr = "The node with ID " + id + " was not found.";
		}

		~NodeNotFoundException() throw() {
		}

		const char* what() const throw() {
			return this->exceptionStr.c_str();
		}

	private:
		std::string exceptionStr;
	};

private:
	// Map from node ID to node.
	typedef std::map <std::string, Node> nodesType;
	nodesType nodes;

	// Map from the ID of link end-points to the edge.
	typedef std::map <Pair <std::string, std::string>, Edge> edgesType;
	edgesType edges;

	bool directed;	// Whether the topology is directed.

};

} //namespace

#endif //TOPOLOGY_H