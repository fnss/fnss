package uk.ac.ucl.ee.fnss;

/**
 * Represent a protocol stack deployed on a node.
 * 
 * A protocol stack is identified by a name and contains a set of properties.
 * 
 * @author Lorenzo Saino
 *
 */
public class ProtocolStack extends NamedPropertyContainer implements Cloneable {

	/**
	 * Constructor
	 * 
	 * @param name the name of the protocol stack
	 */
	public ProtocolStack(String name) {
		super(name);
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
