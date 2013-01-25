"""
Setup script
"""
from distutils.core import setup
import os
import fnss
from fnss import release
# Note: don't need to insert fnss code in the path because by executing this
# script in its directory, the fnss package is already added in the path

# Clean tasks
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

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
            'fnss.traffic'
        ],
        scripts=[
            'bin/fnss-print-debug.py'
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
             'Topic :: Software Development :: Libraries :: Python Modules',
             'Topic :: Scientific/Engineering',
        ],
        description=release.description,
        long_description=fnss.__doc__,  
        requires=[
            "networkx (>= 1.7)",
            "numpy (>= 1.6)"
        ],
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
