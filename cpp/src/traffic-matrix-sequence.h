#ifndef TRAFFIC_MATRIX_SEQUENCE_H
#define TRAFFIC_MATRIX_SEQUENCE_H

#include "traffic-matrix.h"
#include "quantity.h"
#include "units.h"

#include <vector>
#include <exception>
#include <sstream>

namespace fnss {

/**
 * Represent a sequence of traffic matrices, containing traffic matrices
 * referring to a sequence of time intervals.
 * 
 * @author Cosmin Cocora
 */
class TrafficMatrixSequence {
public:
	/**
	 * Constructor.
	 *
	 * @param interval the time interval between traffic matrices.
	 */
	TrafficMatrixSequence(const Quantity &interval = Quantity("1s", Units::Time));

	/**
	 * Get the time interval between traffic matrices.
	 * 
	 * @return the time interval between traffic matrices.
	 */
	Quantity getInterval() const;

	/**
	 * Set the time interval between traffic matrices.
	 *
	 * @param interval the time interval between traffic matrices.
	 */
	void setInterval(const Quantity &interval);

	/**
	 * The size of the sequence.
	 *
	 * @return the number of \c TrafficMatrix objects in the sequence.
	 */
	unsigned int size() const;

	/**
	 * Add a \c TrafficMatrix to the end of the sequence.
	 * 
	 * @param matrix the \c TrafficMatrix to add.
	 */
	void addMatrix(const TrafficMatrix &matrix);

	/**
	 * Add a \c TrafficMatrix at the specified index.
	 * 
	 * If the index exceeds already defined matrices, the sequence is resized to
	 * accommodate the new required size.
	 * 
	 * @param matrix the \c TrafficMatrix to add.
	 * @param index the position in the sequence. 
	 */
	void addMatrix(const TrafficMatrix &matrix, unsigned int index);

	/**
	 * Remove the \c TrafficMatrix at the specified index.
	 * 
	 * Throws an exception if the index is out-of-bounds.
	 * Does not change the sequence index of already existing matrices.
	 *
	 * @param index the position in the sequence.
	 */
	void removeMatrix(unsigned int index);

	/**
	 * Get a copy of the \c TrafficMatrix at the specified index.
	 * 
	 * Throws an exception if the index is out-of-bounds.
	 *
	 * @param index the position in the sequence.
	 */
	TrafficMatrix getMatrix(unsigned int index) const;


	class IndexOutOfBoundsException : public std::exception {
	public:
		IndexOutOfBoundsException(unsigned int index) throw() {
			std::stringstream ss;
			ss<<"The TrafficMatrixSequence index "<<index<<" was out-of-bounds.";
			this->exceptionStr = ss.str();
		}

		~IndexOutOfBoundsException() throw() {
		}

		const char* what() const throw() {
			return this->exceptionStr.c_str();
		}

	private:
		std::string exceptionStr;
	};

private:
	Quantity interval;

	typedef std::vector<TrafficMatrix> sequenceType;
	sequenceType sequence;

};

} //namespace

#endif //TRAFFIC_MATRIX_SEQUENCE_H