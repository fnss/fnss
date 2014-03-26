#!/usr/bin/env python
"""
Generate the .rst files for classes and functions description

"""
import os
import sys
import glob
import inspect
import fnss


def get_subpackages(module):
    dir = os.path.dirname(module.__file__)
    def is_package(d):
        d = os.path.join(dir, d)
        return os.path.isdir(d) and glob.glob(os.path.join(d, '__init__.py*'))

    return filter(is_package, os.listdir(dir))

    
def print_classes(f, outdir):
    outdir = os.path.relpath(outdir, os.path.dirname(f.name))
    classes = inspect.getmembers(fnss, predicate=inspect.isclass)
    for cls_name, cls_type in classes:
        mod_name = cls_type.__module__
        f.write(".. currentmodule:: %s\n" 
                ".. autoclass:: %s.%s\n"
                ".. autosummary::\n"
                "   :toctree: %s/\n\n" % (mod_name, mod_name, cls_name, outdir))
        methods = inspect.getmembers(cls_type)
        method_names = [meth[0] for meth in methods if not meth[0].startswith("_")]
        for meth in method_names:
            f.write("    %s.%s\n" % (cls_name, meth))
        f.write("\n"*2)


def print_functions(f, outdir):
    outdir = os.path.relpath(outdir, os.path.dirname(f.name))
    packages = get_subpackages(fnss)
    for pkg in packages:
        header = ":mod:`%s` package" % pkg
        f.write(header + "\n" + "-"*len(header) + "\n"*2)
        modules = inspect.getmembers(eval('fnss.%s' % pkg), predicate=inspect.ismodule)
        module_names = [mod[0] for mod in modules if not mod[0].startswith("test")]
        module_paths = {}
        for name in module_names:
            fn = eval('fnss.%s.__name__' % name)
            module_paths[fn] = name
        sorted_paths = sorted(module_paths.keys())
        for mod in sorted_paths:
            functions = inspect.getmembers(eval(mod), predicate=inspect.isfunction)
            function_names = [func[0] for func in functions  
                              if (hasattr(eval(mod), '__all__') and func[0] in eval('%s.__all__' % mod))
                             ]
            f.write(".. automodule:: %s.%s.%s\n" 
                    ".. autosummary::\n"
                    "   :toctree: %s/\n\n"  % ('fnss', pkg, module_paths[mod], outdir))
            for func in function_names:
                f.write("    %s\n" % func)
            f.write("\n")
        f.write("\n")


def main(rstfile, outdir):
    """Generate an rst file listing all classes and functions.
    """
    with open(rstfile, 'w+') as f:
        print_classes(f, outdir)
        print_functions(f, outdir)

def usage(name):
    print("Usage: %s inputdir outputdir\n\n" 
          "    inputdir: directory containing the Python code for the examples.\n"
          "    outputdir: directory to put the generated documentation source for these examples.\n" % name)
    sys.exit(-1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])
    main(sys.argv[1], sys.argv[2])