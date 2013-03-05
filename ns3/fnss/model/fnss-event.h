#ifndef FNSS_EVENT_H
#define FNSS_EVENT_H

#include "ns3/event-impl.h"
#include "ns3/object.h"
#include "ns3/core-module.h"

#include <string>

namespace ns3 {

/**
 * Overrides the inheritance pattern of EventImp to make use of the object factory
 * facilities provided by ns3::Object. All events that need to be crated from a
 * fnss::EventSchedule should inherit from this class.
 */
class FNSSEvent : public Object, public EventImpl {
public:
	static TypeId GetTypeId (void);

	FNSSEvent();

	virtual ~FNSSEvent();

	virtual void Notify();

	/**
	 * Avoid inheritance ambiguity.
	 */
	void Unref() {
		EventImpl::Unref();
	}

	/**
	 * Avoid inheritance ambiguity.
	 */
	void Ref() {
		EventImpl::Unref();
	}

private:
	std::string m_eventId;
};

}

#endif