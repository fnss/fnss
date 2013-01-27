package uk.ac.ucl.ee.fnss;

/**
 * Represent an application deployed on a node.
 *
 * An application is identified by a name and contains a set of properties.
 *
 * @author Lorenzo Saino
 *
 */
public class Application extends NamedPropertyContainer implements Cloneable {

	/**
	 * Constructor
	 * 
	 * @param name the name of the application
	 */
	public Application(String name) {
		super(name);
	}

	/**
	 * Return a copy of this object
	 * 
	 * @return A copy of this object
	 */
	@Override
	public Application clone() {
		return (Application) super.clone();
	}
}
