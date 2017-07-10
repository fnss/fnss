"""
Dynamic topology
================

This example shows how to generate a topology, an event schedule and a traffic
matrix.

In this specific example we create a Waxman topology and create an event
schedule listing random link failures and restores and generate a static
traffic matrix.

This scenario could be used to assess the performance of a routing algorithm
in case of frequent link failures.
"""
import fnss
import random

# generate a Waxman1 topology with 200 nodes
topology = fnss.waxman_1_topology(n=200, alpha=0.4, beta=0.1, L=1)

# assign constant weight (1) to all links
fnss.set_weights_constant(topology, 1)


# set delay equal to 1 ms to all links
fnss.set_delays_constant(topology, 1, 'ms')

# set varying capacities among 10, 100 and 1000 Mbps proprtionally to edge
# betweenness centrality
fnss.set_capacities_edge_betweenness(topology, [10, 100, 1000], 'Mbps')


# now create a static traffic matrix assuming all nodes are both origins
# and destinations of traffic
traffic_matrix = fnss.static_traffic_matrix(topology, mean=2, stddev=0.2, max_u=0.5)

# This is the event generator function, which generates link failure events
def rand_failure(links):
    link = random.choice(links)
    return {'link': link, 'action': 'down'}

# Create schedule of link failures
event_schedule = fnss.poisson_process_event_schedule(
                        avg_interval=0.5,  # 0.5 min = 30 sec
                        t_start=0,  # starts at 0
                        duration=60,  # 2 hours
                        t_unit='min',  # minutes
                        event_generator=rand_failure,  # event gen function
                        links=topology.edges(),  # 'links' argument
                        )

# Now let's create a schedule with link restoration events
# We assume that the duration of a failure is exponentially distributed with
# average 1 minute.
restore_schedule = fnss.EventSchedule(t_start=0, t_unit='min')
for failure_time, event in event_schedule:
    link = event['link']
    restore_time = failure_time + random.expovariate(1)
    restore_schedule.add(time=restore_time,
                         event={'link': link, 'action': 'up'},
                         absolute_time=True
                         )

# Now merge failure and restoration schedules
# After merging events are still chronologically sorted
event_schedule.add_schedule(restore_schedule)

# Note: there are several ways to create this link failure-restoration schedule
# This method has been used to illustrate a variety of functions and methods
# that FNSS provides to manipulate event schedules

# Write topology, event schedule and traffic matrix to files
fnss.write_topology(topology, 'topology.xml')
fnss.write_event_schedule(event_schedule, 'event_schedule.xml')
fnss.write_traffic_matrix(traffic_matrix, 'traffic_matrix.xml')



