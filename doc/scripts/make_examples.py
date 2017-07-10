#!/usr/bin/env python
"""
Script to generate RST files from Python example files.

This script is partially based on a script from the Matplotlib project.
"""
import os
import sys


TITLE_STYLE = ("=", '-', '^')

def make_rst(inpath, outpath):
    """Convert Python source file into RST file

    Parameters
    ----------
    inpath : str
        Path to the input .py file
    outpath: str
        Path to the output .rst file
    """
    with open(inpath, 'r') as infile:
        with open(outpath, 'w+') as outfile:
            base = os.path.basename(inpath).partition('.')[0]
            title = "%s" % base.replace('_', ' ').title()
            outfile.write(title + '\n' +
                          '=' * len(title) + '\n' * 2 +
                          '::\n\n')
            for line in infile:
                outfile.write(' ' * 4 + line)


def main(indir, outdir):
    """Create RST files from Python code

    indir : str
        Directory where example .py files are located
    outdir: str
        Directory in which output .rst files will be located
        This folder will be created if it does not exist
    """
    # Create outdir if does not exist
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    # Create and open index.rst in target dir
    with open(os.path.join(outdir, 'index.rst'), 'w+') as index:
        index.write("********\n"
                    "Examples\n"
                    "********\n\n"
                    ".. toctree::\n"
                    "    :maxdepth: 2\n\n")
        # Iterate over the Python file directory
        for root, subdirs, files in os.walk(indir):
            files = [f for f in files if f[0] not in ('.', '#', '_') and f.endswith('.py')]
            if not files:  # Empty directory
                continue
            # create subdirectory in outdir if it is not the root
            relpath = os.path.relpath(root, start=indir)
            outsubdir = os.path.join(outdir, relpath)
            if root != indir:
                os.mkdir(outsubdir)
                level = relpath.count(os.sep)
                title = os.path.basename(relpath).replace('_', ' ').title()
                index.write("\n" + title + "\n" + TITLE_STYLE[level - 1] * len(title) + "\n"*2 +
                            ".. toctree::\n"
                            "    :maxdepth: 2\n\n")
            # Create files in target output directory
            for f in files:
                reloutfile = os.path.join(relpath, f.rstrip('py') + 'rst')
                make_rst(os.path.join(root, f), os.path.join(outdir, reloutfile))
                index.write("    %s\n" % reloutfile)


def usage(name):
    print("Usage: %s inputdir outputdir\n\n"
          "    inputdir: directory containing the Python code for the examples.\n"
          "    outputdir: directory to put the generated documentation source for these examples.\n" % name)
    sys.exit(-1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])
    main(sys.argv[1], sys.argv[2])

