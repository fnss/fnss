#!/usr/bin/env python
import os
import sys
import pkg_resources as pkg

# list of FNSS dependencies, including FNSS itself
packages = ['fnss',
            'networkx',
            'numpy',
            'scipy',
            'nose',
            'sphinx',
            'numpydoc',
            ]

if __name__ == "__main__":
    sysname, nodename, release, version, machine = os.uname()
    py_version = sys.version
    print('[INFO] OS sysname: %s' % sysname)
    print('[INFO] OS release: %s' % release)
    print('[INFO] OS version: %s' % version)
    print('[INFO] Machine: %s' % machine)
    print('[INFO] Python version: %s' % py_version.replace('\n', ''))

    # see what packages and versions are installed    
    for package in packages:
        try:
            version = pkg.get_distribution(package).version
            print('[INFO] %s: installed with distutils' % package)
            print('[INFO] %s: version: %s' % (package, version))
        except pkg.DistributionNotFound:
            try:
                exec('import %s' % package)
                print('[INFO] %s: installed manually' % package)
                if hasattr(eval(package), '__version__'):
                    version = eval('%s.__version__' % package)
                    print('[INFO] %s: version: %s' % (package, version))
                else:
                    print('[INFO] %s: version unknown' % package)
                exec('del %s' % package)
            except ImportError:
                print ('[ERROR] Cannot import %s package' % package)
