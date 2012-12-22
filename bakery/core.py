""" Core API """

import glob
import imp
import os

_SCRIPTDIR =  os.path.dirname(os.path.realpath(__file__))
_EXTROOT = os.path.join(_SCRIPTDIR, 'ext')

extensions = { }

def load_extensions():
    """ 
    Searches _EXTROOT for C extensions and loads them into the current
    interpreter. Returns a dictionary from the extension's module name to the
    module itself.
    """

    print "Loading extensions..."
    ext = { }

    for pattern in [ '*.so', '*.pyo', '*.pyc' ]:
        for module in glob.glob(os.path.join(_EXTROOT, pattern)):
            try:
                name = os.path.basename(module)
                name = os.path.splitext(name)[0]
                if name == '__init__':
                    continue

                name = 'bakery.ext.' + name
                print "   ", name, "...",

                ext[name] = imp.load_dynamic(name, module)
                print "ok"
            except:
                print "error (not a module?)"

    global extensions
    extensions = ext

def import_asset(TODO, arglist):
    pass

def process_asset(TODO, arglist):
    pass

def export_asset(TODO, arglist):
    pass

# TODO
# - core module
# - buildchain module
# - bakefile module
# - Documentation for building extensions
# - Build a couple of dummy core extensions
# - Load build chain
# - Validate build chain
# - Load extensions for build chain
# - Generate assets
# - Generate source files for loading the assets
# - Setup stuff
# - Setup instructions
# - List of core extensions
# - Core extensions

