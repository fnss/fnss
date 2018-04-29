"""
Export topology to ns-2
=======================

This example shows how to generate a topology (a line in this case) and export
it to the ns-2 simulator
"""
import fnss

# create a line topology with 10 nodes
topology = fnss.line_topology(10)

# assign capacity of 10 Mbps to each link
fnss.set_capacities_constant(topology, 10, 'Mbps')

# assign delay of 2 ms to each link
fnss.set_delays_constant(topology, 2, 'ms')

# set buffers in each node (use packets, bytes not supported by ns-2)
fnss.set_buffer_sizes_bw_delay_prod(topology, 'packets', 1500)

# Add FTP application to first and last node of the line
tcp_stack_props = {'class': 'Agent/TCP', 'class_': 2, 'fid_': 1}
fnss.add_stack(topology, 0, 'tcp', tcp_stack_props)
fnss.add_stack(topology, 9, 'tcp', tcp_stack_props)

ftp_app_props = {'class': 'Application/FTP', 'type': 'FTP'}
fnss.add_application(topology, 0, 'ftp', ftp_app_props)
fnss.add_application(topology, 9, 'ftp', ftp_app_props)

# export topology to a Tcl script for ns-2
fnss.to_ns2(topology, 'ns2-script.tcl', stacks=True)
