#ifndef PAIR_H
#define PAIR_H

#include <utility>

namespace fnss {

// You get operators !=,<=,>,>= if you define operators < and == and inherit from
// this class using your class as the template parameter. Possible
template <typename D>
class RelOP {
public:
  RelOP() : derived(*static_cast<const D*>(this)) {}
  bool operator!=(const D &rhs) const {
    return !(derived == rhs);
  }

  bool operator<=(const D &rhs) const {
    return derived < rhs || derived == rhs;
  }

  bool operator>(const D &rhs) const {
    return !(derived < rhs) && !(derived == rhs);
  }

  bool operator>=(const D &rhs) const {
    return !(derived > rhs);
  }

private:
  const D& derived;
};

/**
 * Wrapper class for std::pair that adds optional commutativity to the pair,
 * eg. the pairs <1, 2> and <2, 1> will return true for operator==(..) if the
 * commutative flag is set. You _can_ use T1 != T2, but operators == and <,
 *
 * @author Cosmin Cocora
 */
template <class T1, class T2> class Pair : public RelOP<Pair<T1, T2> >{
public:
	T1 &first;
	T2 &second;

	Pair(bool commutative_ = false) :
		first(stlPair.first), second(stlPair.second), stlPair(), commutative(commutative_) {}

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

	std::pair<T1, T2> getStlPair() const {
		return this->stlPair;
	}

	bool getCommutative() const {
		return this->commutative;
	}

	void setCommutative(bool commutative) {
		this->commutative = commutative;
	}

	Pair& operator=(const Pair &rhs) {
		this->stlPair = rhs.stlPair;

		return *this;
	}

	bool operator==(const Pair &rhs) const {
		if(this->commutative || rhs.commutative) {
			if((this->first == rhs.first && this->second == rhs.second) ||
				(this->second == rhs.first && this->first == rhs.second))
				return true;
			else
				return false;
		} else {
			return this->stlPair == rhs.stlPair;
		}
	}

	bool operator<(const Pair &rhs) const {
		if (this->commutative || rhs.commutative) {
			if (this->first < this->second) {
				if (rhs.first < rhs.second)
					return this->first < rhs.first || (this->first == rhs.first && this->second < rhs.second);
				else
					return this->first < rhs.second || (this->first == rhs.second && this->second < rhs.first);
			} else {
				if (rhs.first < rhs.second)
					return this->second < rhs.first || (this->second == rhs.first && this->first < rhs.second);
				else
					return this->second < rhs.second || (this->second == rhs.second && this->first < rhs.first);
			}
		} else {
			return this->first < rhs.first || (this->first == rhs.first && this->second < rhs.second);
		}
	}

private:
	std::pair <T1, T2> stlPair;
	bool commutative;
};

} //namespace

#endif //PAIR_H
