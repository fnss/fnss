Scripts
=======

mn-fnss
-------

Usage::

  mn-fnss [options] <topology-file>
  mn-fnss (--help | -h)

Launch Mininet console with an FNSS topology.

This script parses an FNSS topology XML file and launches the Mininet console
passing this topology.

This script accepts all the options of Mininet *mn* script, except for the
*custom* and *topo* options which are overwritten by this script.

In addition, if the user specifies the mn *link* option, then all potential
link attributes of the topology (e.g. capacity, delay and max queue size) are
discarded and values provided with the link attributes are used instead.

Unless used to get this help message, this script must be run as superuser.

Example usage::

  $ python
  >>> import fnss
  >>> topo = fnss.two_tier_topology(1, 2, 2)
  >>> fnss.write_topology(topo, 'fnss-topo.xml')
  $ sudo mn-fnss fnss-topo.xml


fnss-troubleshoot
-----------------

Usage::

  fnss-troubleshoot [--help | -h]

This script prints debugging information about FNSS dependencies currently
installed.

The main purpose of this script is to help users to communicate effectively
with developers when reporting an issue.
