#!/bin/sh
#
# This script automatically downloads and installs the FNSS core library along with all its dependencies
#
# This script has been tested only on Ubuntu version 12.04+
#

# Makes sure all packages installed are up-to-date
sudo apt-get update
sudo apt-get upgrade

# Install all dependencies available on Ubuntu package repository
sudo apt-get install python python-pip python-setuptools python-numpy python-networkx python-mako python-nose

# Install other optional dependencies not available on Ubuntu package repository
sudo pip install sphinx numpydoc

# Install FNSS core library
sudo pip install fnss