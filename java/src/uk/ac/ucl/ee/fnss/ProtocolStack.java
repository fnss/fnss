package uk.ac.ucl.ee.fnss;

/**
 * Represent a protocol stack deployed on a node.
 * 
 * A protocol stack is identified by a name and contains a set of properties.
 * 
 * @author Lorenzo Saino
 *
 */
public class ProtocolStack extends PropertyContainer implements Cloneable {

	private String name = null;

	/**
	 * Constructor
	 * 
	 * @param name the name of the protocol stack
	 */
	public ProtocolStack(String name) {
		this.name = name;
	}
	
	/**
	 * Return the name of the protocol stack
	 * 
	 * @return the name of the stack
	 */
	public String getName() {
		return name;
	}

	/**
	 * Set the name of the protocol stack
	 * 
	 * @param name the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}
	
	/**
	 * Return a copy of this object
	 * 
	 * @return A copy of this object
	 */
	@Override
	public ProtocolStack clone() {
		return (ProtocolStack) super.clone();
	}
}
