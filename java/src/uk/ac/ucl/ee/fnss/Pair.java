package uk.ac.ucl.ee.fnss;

/**
 * A class containing a pair of objects U and V
 * 
 * @author Lorenzo Saino
 *
 * @param <U> The type of the first element of the pair
 * @param <V> The type of the second element of the pair
 */
public class Pair <U, V> {

	private final U u;
	private final V v;
	private transient final int hash;

	/**
	 * Constructor
	 * 
	 * @param u the first object of the pair
	 * @param v the second object of the pair
	 */
	public Pair(U u, V v) {
		this.u = u;
		this.v = v;
		this.hash = (u == null ? 0 : u.hashCode() * 31)
				+ (v == null ? 0 : v.hashCode());
	}

	/**
	 * Return the first object of the pair
	 * 
	 * @return the first object of the pair
	 */
	public U getU() {
		return u;
	}

	/**
	 * Return the second object of the pair
	 * 
	 * @return the second object of the pair
	 */
	public V getV() {
		return v;
	}

    /**
     * Returns a hash code value for the object. This method is
     * supported for the benefit of hashtables such as those provided by
     * <code>java.util.Hashtable</code>.
     * 
     * @return  a hash code value for this object.
     * @see     #equals(java.lang.Object)
     * @see     java.util.Hashtable
     */
	@Override
	public int hashCode() {
		return hash;
	}

    /**
     * Indicates whether some other object is "equal to" this one.
     *
     * @param   object   the reference object with which to compare.
     * @return  <code>true</code> if this object is the same as the object
     *          argument; <code>false</code> otherwise.
     * @see     #hashCode()
     */
	@Override
	public boolean equals(Object object) {
		if (object == this) {
			return true;
		} else	if (object == null || !getClass().isInstance(object)) {
			return false;
		}
		@SuppressWarnings("unchecked")
		Pair<U, V> other = getClass().cast(object);
		return (u == null ? other.u == null : u.equals(other.u))
				&& (v == null ? other.v == null : v.equals( other.v));
	}
}
