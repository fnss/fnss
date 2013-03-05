#include "fnss-event.h"

#include "ns3/string.h"
#include "ns3/log.h"

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("FNSSEvent");
NS_OBJECT_ENSURE_REGISTERED (FNSSEvent);

TypeId FNSSEvent::GetTypeId (void) {
  static TypeId tid = TypeId ("ns3::FNSSEvent")
    .SetParent(Object::GetTypeId())
    .AddConstructor<FNSSEvent> ()
    .AddAttribute ("event_id", 
                   "ID of the event",
                   StringValue ("Unknown Event"),
                   MakeStringAccessor (&FNSSEvent::m_eventId),
                   MakeStringChecker());

  return tid;
}

FNSSEvent::FNSSEvent() {

}

FNSSEvent::~FNSSEvent() {

}

void FNSSEvent::Notify() {
	NS_LOG_INFO(this->m_eventId);
}

}