#ifndef COMMUTATIVE_PAIR_H
#define COMMUTATIVE_PAIR_H

#include "pair.h"

namespace fnss {

template <class T1, class T2> class CommutativePair : public Pair<T1, T2> {
public:
	bool operator==(const Pair<T1, T2> &other) {
		if((this->first == other.first && this->second == other.second) ||
			(this->second == other.first && this->first == other.second))
			return true;
		else
			return false;
	}
};

} //namespace

#endif //COMMUTATIVE_PAIR_H