package uk.ac.ucl.ee.fnss;

/**
 * Represent an application deployed on a node.
 *
 * An application is identified by a name and contains a set of properties.
 *
 * @author Lorenzo Saino
 *
 */
public class Application extends PropertyContainer implements Cloneable {

	private String name = null;

	/**
	 * Constructor
	 * 
	 * @param name the name of the application
	 */
	public Application(String name) {
		this.name = name;
	}

	/**
	 * Return the name of the application
	 * 
	 * @return the name of the application
	 */
	public String getName() {
		return name;
	}

	/**
	 * Set the name of the application
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
	public Application clone() {
		return (Application) super.clone();
	}

}
