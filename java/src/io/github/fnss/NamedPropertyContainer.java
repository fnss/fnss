package io.github.fnss;

/**
 * Named property container.
 * 
 * This object is simply a generic property container mapped to a name
 * 
 * @author Lorenzo Saino
 *
 */
public class NamedPropertyContainer extends PropertyContainer implements Cloneable {

	private String name = null;

	/**
	 * Constructor
	 * 
	 * @param name the name of the object
	 */
	public NamedPropertyContainer(String name) {
		this.name = name;
	}
	
	/**
	 * Return the name of this object
	 * 
	 * @return the name of the property container
	 */
	public String getName() {
		return name;
	}

	/**
	 * Set the name of this object
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
	public NamedPropertyContainer clone() {
		return (NamedPropertyContainer) super.clone();
	}
}
