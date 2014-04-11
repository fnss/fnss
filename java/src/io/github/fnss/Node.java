package io.github.fnss;

import java.util.Hashtable;
import java.util.Map;
import java.util.Set;

/**
 * Represent a node of a topology.
 * 
 * Each node comprises a set of properties (e.g. if the node is a router/switch
 * or host) and a set of protocol stacks.
 *
 * @author Lorenzo Saino
 */
public class Node extends PropertyContainer implements Cloneable {

	private ProtocolStack protocolStack = null;
	private Map<String, Application> applications = 
			new Hashtable<String, Application>();

	/**
	 * Constructor
	 */
	public Node() { }
	
	/**
	 * Constructor
	 *
	 * <br>
	 * Note: the protocol stack object actually deployed on the node is a copy
	 * of the stack passed as argument. Therefore, any changes in the object
	 * after invoking this method do not have any effect on the stack deployed 
	 * on the node.
	 *
	 * @param stack The protocol stack of the node.
	 */
	public Node(ProtocolStack stack) {
		setProtocolStack(stack);
	}

	/**
	 * Return the protocol stack deployed on the node
	 * 
	 * @return the <code>ProtocolStack</code> object, if present. Otherwise, 
	 * <code>null</code> is returned.
	 * @see ProtocolStack
	 */
	public ProtocolStack getProtocolStack() {
		return protocolStack;
	}
	
	/**
	 * Deploy the specified protocol stack on the node. If node there is already
	 * a protocol stack with the same name deployed, that is overwritten. 
	 * <br>
	 * Note: the protocol stack object actually deployed on the node is a copy
	 * of the stack passed as argument. Therefore, any changes in the object
	 * after invoking this method do not have any effect on the stack deployed 
	 * on the node.
	 * 
	 * @param stack The protocol stack to deploy
	 * 
	 * @see ProtocolStack
	 */
	public void setProtocolStack(ProtocolStack stack) {
		this.protocolStack = stack.clone();
	}

	/**
	 * Removes the protocol stack deployed on the node, if any.
	 * 
	 * It is equivalent to set the protocol stack to <code>null</code> with
	 * the <code>setProtocolStack</code> method.
	 * 
	 * @see Node#setProtocolStack(ProtocolStack)
	 */
	public void removeProtocolStack() {
		this.protocolStack = null;
	}

	/**
	 * Return the application with the specified name
	 * 
	 * @param name the name of the application
	 * @return the <code>Application</code> object, if present. Otherwise, 
	 * <code>null</code> is returned.
	 * @see Application
	 */
	public Application getApplication(String name) {
		return applications.get(name);
	}
	
	/**
	 * Return a set containing all the application names. To get the object of 
	 * a specific application use <code>getApplication(String)</code>
	 * 
	 * @return a set with all names of applications deployed on this node
	 * 
	 * @see #getApplication(String)
	 */
	public Set<String> getAllApplications() {
		return applications.keySet();
	}
	
	/**
	 * Deploy the specified application on the node. If node there is already
	 * an application with the same name deployed, that is overwritten. 
	 * <br>
	 * Note: the application object actually deployed on the node is a copy
	 * of the application passed as argument. Therefore, any changes in the
	 * object after invoking this method do not have any effect on the
	 * application deployed on the node.
	 *
	 * @param application The application to deploy
	 * @see Application
	 */
	public void setApplication(Application application) {
		application = application.clone();
		applications.put(application.getName(), application);
	}

	/**
	 * Remove a specific application from the node
	 *
	 * @param name The name of the application to remove
	 * @return The removed <code>Application</code> object, if was present
	 * on the node. Otherwise <code>null</code> is returned.
	 */
	public Application removeApplication(String name) {
		return applications.remove(name);
	}

	/**
	 * Return a copy of this object
	 * 
	 * @return A copy of this object
	 */
	@Override
	public Node clone() {
		Node clone = (Node) super.clone();
		if (protocolStack != null) {
			protocolStack = protocolStack.clone();
		}
		for (String key : applications.keySet()) {
			applications.put(key, applications.get(key).clone());
		}
		return clone;
	}
}
