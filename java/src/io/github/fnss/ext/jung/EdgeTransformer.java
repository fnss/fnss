package io.github.fnss.ext.jung;

import io.github.fnss.Edge;

import org.apache.commons.collections15.Transformer;

/**
 * Transformer converting an FNSS Edge object into the value of its requested
 * attributes.
 * 
 * This transformer is needed by a number of JUNG algorithms.
 * 
 * @author Lorenzo Saino
 */
public class EdgeTransformer implements Transformer<Edge, Number> {

	/**
	 * Link capacity property name
	 */
	public static final String CAPACITY = "capacity";
	
	/**
	 * Link delay property name
	 */
	public static final String DELAY = "delay";
	
	/**
	 * Link weight property name
	 */
	public static final String WEIGHT = "weight";
	
	private String property = null;

	/**
	 * Constructor.
	 * 
	 * @param property The name of the edge property that is expected from the
	 * transformer
	 */
	public EdgeTransformer(String property) {
		this.property = property;
	}
	
	/**
	 * Return the value of the edge property specified when instantiating the
	 * the object.
	 * 
	 * If the edge does not have the specified property, then the method returns
	 * <code>null</code>.
	 * 
	 * @param edge The edge to be transformed
	 * @return The value of the property
	 */
	@Override
	public Number transform(Edge edge) {
		if (property.equals(CAPACITY)) {
			return edge.getCapacity();
		} else if (property.equals(DELAY)) {
			return edge.getDelay();
		} else if (property.equals(WEIGHT)) {
			return edge.getWeight();
		} else {
			return (edge.getProperty(property) == null) ? null : new Float(edge.getProperty(property));
		}
	}

}
