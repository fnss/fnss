package uk.ac.ucl.ee.fnss;

import java.util.Hashtable;
import java.util.Map;
import java.util.Set;

/**
 * Generic container for properties
 *
 * @author Lorenzo Saino
 *
 */
public class PropertyContainer implements Cloneable {

	private Map<String, String> properties = new Hashtable<String, String>();

	/**
	 * Constructor
	 */
	public PropertyContainer() { }

	/**
	 * Return the value of a specific edge property
	 *
	 * @param name The name of the property
	 *
	 * @return The value of the property, if present. Otherwise, 
	 * <code>null</code> is returned.
	 */
	public String getProperty(String name) {
		return properties.get(name);
	}

	/**
	 * Set the value of a specific edge property. If a property with the same
	 * name already exists, it is overwritten
	 *
	 * @param name The name of the property
	 * @param value The value of the property
	 */
	public void setProperty(String name, String value) {
		properties.put(name, value);
	}

	/**
	 * Remove a specific property
	 * 
	 * @param name The name of the property to remove
	 * 
	 * @return the value of the property removed or <code>null</code> if no
	 * property with the given name was present. 
	 */
	public String removeProperty(String name) {
		return properties.remove(name);
	}
	
	/**
	 * Return a set containing all the property names. To get the value of a
	 * specific property use <code>getProperty(String name)</code>
	 * 
	 * @return a set with all property names of the object
	 * 
	 * @see #getProperty(String)
	 */
	public Set<String> getAllProperties() {
		return properties.keySet();
	}


	/**
	 * Return a copy of this object
	 * 
	 * @return A copy of this object
	 */
	@SuppressWarnings("unchecked")
	@Override
	public PropertyContainer clone() {
		PropertyContainer clone = null;
		try {
			clone = (PropertyContainer) super.clone();
		} catch (CloneNotSupportedException e) {
			/*
			 * It is safe to swallow the exception because Edge implements
			 * the cloneable interface, therefore this exception will never
			 * be thrown
			 */
			return null;
		}
		// deep copy property map otherwise this object and the clone
		// will point to the same properties object
		properties = (Map<String, String>)
				((Hashtable<String, String>) properties).clone();
		return clone;
	}

}
