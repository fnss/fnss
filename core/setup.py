"""
Setup script
"""
import sys
import os
from shutil import rmtree

# Verify Python version
if sys.version_info[:2] < (2, 6):
    print("FNSS requires Python version 2.6 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

# Packages required to run FNSS
required_packages = [('networkx', '>=', '1.6'),
                     ('numpy', '>=', '1.4'),
                     ('mako', '>=', '0.4')]

# Packages required to run tests and build documentation
optional_packages = [('nose', '>=', '1.1'),
                     ('numpydoc', '>=', '0.4'),
                     ('sphinx', '>=', '1.1')]

# Python 2.6 version of unittest does not include features required by
# FNSS's tests: unittest2 is needed 
if sys.version_info[:2] == (2, 6):
    optional_packages.append(('unittest2', '>=', '0.4'))

# if install in development mode, then install all packages required to
# run tests and build documentation
if sys.argv[-1] == 'develop':
    required_packages += optional_packages

# Try using setuptools if available. It would take care of automatically
# downloading all required dependencies and installing them.
# If it is not available, the script falls back to distutils, which is
# part of Python standard library but does not automatically
# install missing packages. In this case, the script manually checks
# for all dependencies and if any are missing, prints an error message
# and exits
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    from distutils.version import LooseVersion
    for package, condition, req_version in required_packages:
        try:
            exec('import %s' % package)
            installed_version = eval('%s.__version__' % package)
            if not eval('LooseVersion(\'%s\') %s LooseVersion(\'%s\')' 
                        % (installed_version, condition, req_version)):
                print('FNSS requires package %s, version %s %s '
                      '(%s detected). Update package and try again' 
                      % (package, condition, req_version, installed_version))
                sys.exit(-1)
        except ImportError:
            print ('FNSS requires package %s, which is not installed. '
                   'Install it and try again' % package)
            sys.exit(-1)

# It imports release module this way because if it tried to import fnss package
# and some required dependencies were not installed, that would fail
# This is the only way to access the release module without needing all
# dependencies.
sys.path.insert(0, 'fnss')
import release
sys.path.pop(0)

# Clean tasks
if os.path.exists('MANIFEST'): os.remove('MANIFEST')
if os.path.exists('fnss.egg-info'): rmtree('fnss.egg-info')

# Main scripts
if __name__ == "__main__":
    setup(
        name='fnss',
        version=release.version,
        author=release.author,
        author_email=release.author_email,
        packages=[
            'fnss',
            'fnss.netconfig',
            'fnss.topologies',
            'fnss.traffic',
            'fnss.adapters',
        ],
        scripts=[
            'bin/fnss-troubleshoot',
            'bin/mn-fnss'
        ],
        url=release.url,
        download_url=release.download_url,
        license=release.license_long,
        classifiers=[
             'Development Status :: 4 - Beta',
             'Intended Audience :: Developers',
             'Intended Audience :: Science/Research',
             'Intended Audience :: Telecommunications Industry',
             'License :: OSI Approved :: BSD License',
             'Natural Language :: English',
             'Operating System :: OS Independent',
             'Programming Language :: Python :: 2',
             'Programming Language :: Python :: 2.6',
             'Programming Language :: Python :: 2.7',
             'Programming Language :: Python :: 3',
             'Programming Language :: Python :: 3.1',
             'Programming Language :: Python :: 3.2',
             'Programming Language :: Python :: 3.3',
             'Topic :: Software Development :: Libraries :: Python Modules',
             'Topic :: Scientific/Engineering',
        ],
        description=release.description_short,
        long_description=release.description_long,
        requires=['%s (%s%s)' % (pkg, cond, ver)
                  for pkg, cond, ver in required_packages],
        install_requires=['%s%s%s' % (pkg, cond, ver)
                          for pkg, cond, ver in required_packages],
        keywords=[
            'network',
            'simulation',
            'topology',
            'traffic matrix', 
            'link capacity',
            'delay',
            'protocol stack'
        ]
    )
