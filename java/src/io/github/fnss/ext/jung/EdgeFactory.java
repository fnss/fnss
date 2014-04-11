package io.github.fnss.ext.jung;

import io.github.fnss.Edge;

import org.apache.commons.collections15.Factory;


/**
 * Edge factory for JUNG graphs.
 * 
 * This class is a factory of FNSS <code>Edge</code> objects which can be used
 * to manipulate JUNG graphs generated from FNSS <code>Topology</code> objects. 
 * 
 * @author Lorenzo Saino
 *
 */
public class EdgeFactory implements Factory<Edge> {

	/**
	 * Constructor
	 */
	public EdgeFactory() {}
	
	/**
	 * Create an <code>Edge</code> object
	 * 
	 * @return the edge
	 */
	@Override
	public Edge create() {
		return new Edge();
	}
	
}
