#!/usr/bin/env python

import glob
import imp
import os

_SCRIPTDIR =  os.path.dirname(os.path.realpath(__file__))
_EXTROOT = os.path.join(_SCRIPTDIR, 'ext')

def load_extensions():
    print "Loading extensions..."
    ext = [ ]

    for module in glob.glob(os.path.join(_EXTROOT, '*.so')):
        try:
            name = 'bakery.ext.%s' % os.path.basename(module)[:-len('.so')]
            print "   ", name, "...",
            ext.append(imp.load_dynamic(name, module))
            print "ok"
        except:
            print "error (not a module?)"

    return ext


# TODO
# - Container object for intermediate asset objects
#   (wraps C++ data, provides type safety)
# - Container object for build chain items
# - Figure out how we're going to search for and load extensions
# - Figure out how we're going to specify build chains (Bakefiles?)
# - Documentation for building extensions
# - Build a couple of dummy core extensions
# - Load build chain
# - Validate build chain
# - Load extensions for build chain
# - Generate assets
# - Generate source files for loading the assets
# - Figure out how to set up python packages
# - Setup stuff
# - Setup instructions
# - List of core extensions
# - Core extensions

