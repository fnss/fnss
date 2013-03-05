#ifndef PAIR_H
#define PAIR_H

#include <utility>

namespace fnss {

/**
 * Wrapper class for std::pair that adds optional commutativity to the pair,
 * eg. the pairs <1, 2> and <2, 1> will return true for operator==(..) if the
 * commutative flag is set.
 *
 * @author Cosmin Cocora
 */
template <class T1, class T2> class Pair {
public:
	Pair(bool commutative = false) :
		first(stlPair.first), second(stlPair.second), stlPair() {

		this->commutative = commutative;
	}

	Pair(const T1 &first, const T2 &second, bool commutative = false) :
		first(stlPair.first), second(stlPair.second), stlPair(first, second) {

		this->commutative = commutative;
	}

	Pair(const std::pair <T1, T2> &p, bool commutative = false) :
		first(stlPair.first), second(stlPair.second), stlPair(p) {

		this->commutative = commutative;
	}

	Pair(const Pair<T1, T2> &other) :
		first(stlPair.first), second(stlPair.second), stlPair(other.stlPair) {

		this->commutative = other.commutative;
	}

	T1 &first;
	T2 &second;

	std::pair<T1, T2> getStlPair() const {
		return this->stlPair;
	}

	bool getCommutative() const {
		return this->commutative;
	}

	void setCommutative(bool commutative) {
		this->commutative = commutative;
	}

	Pair& operator=(const Pair &other) {
		this->stlPair = other.stlPair;

		return *this;
	}

	bool operator==(const Pair &other) const {
		if(this->commutative || other.commutative) {
			if((this->first == other.first && this->second == other.second) ||
				(this->second == other.first && this->first == other.second))
				return true;
			else
				return false;
		} else {
			return this->stlPair == other.stlPair;
		}
	}

	bool operator!=(const Pair &other) const {
		return !(*this == other);
	}

	bool operator<(const Pair &other) const {
		return (this->stlPair < other.stlPair) && !(*this == other);
	}

	bool operator<=(const Pair &other) const {
		return (this->stlPair < other.stlPair) || (*this == other);
	}

	bool operator>=(const Pair &other) const {
		return (this->stlPair > other.stlPair) || (*this == other);
	}

	bool operator>(const Pair &other) const {
		return this->stlPair > other.stlPair && !(*this == other);
	}

private:
	std::pair <T1, T2> stlPair;
	bool commutative;
};

} //namespace

#endif //PAIR_H