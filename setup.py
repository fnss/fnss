"""Setup script"""
import sys
import os
from shutil import rmtree

from setuptools import setup, find_packages

# Packages required to run FNSS
requires = [
    'networkx (>=1.6)',
    'numpy (>=1.4)',
    'mako (>=0.4)'
]

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
        packages=find_packages(exclude=("test*",)),
        scripts=[
            'bin/fnss-troubleshoot',
            'bin/mn-fnss'
        ],
        url=release.url,
        download_url=release.download_url,
        license=release.license_long,
        classifiers=[
             'Development Status :: 5 - Production/Stable',
             'Intended Audience :: Developers',
             'Intended Audience :: Science/Research',
             'Intended Audience :: Telecommunications Industry',
             'License :: OSI Approved :: BSD License',
             'Natural Language :: English',
             'Operating System :: OS Independent',
             'Programming Language :: Python :: 2',
             'Programming Language :: Python :: 2.7',
             'Programming Language :: Python :: 3',
             'Programming Language :: Python :: 3.4',
             'Programming Language :: Python :: 3.5',
             'Programming Language :: Python :: 3.6',
             'Topic :: Software Development :: Libraries :: Python Modules',
             'Topic :: Scientific/Engineering',
        ],
        description=release.description_short,
        long_description=release.description_long,
        python_requires='>=2.7.9, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
        install_requires=requires,
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
