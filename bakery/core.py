""" Core API """

import glob
import os

from imp import load_dynamic

_SCRIPTDIR =  os.path.dirname(os.path.realpath(__file__))
_EXTROOT = os.path.join(_SCRIPTDIR, 'ext')

extensions = { }    # extension name => module object
importers = { }     # importer name => (list(file extensions), callback)
processors = { }    # processor name => callback
exporters = { }     # exporter name => callback

def load_extensions():
    """ 
    Searches _EXTROOT for C extensions and loads them into the current
    interpreter. Returns a dictionary from the extension's module name to the
    module itself.
    """

    print "Loading extensions..."
    global extensions
    global importers
    global processors
    global exporters

    for pattern in [ '*.so', '*.pyo', '*.pyc' ]:
        for module in glob.glob(os.path.join(_EXTROOT, pattern)):
            try:
                name = os.path.basename(module)
                name = os.path.splitext(name)[0]
                if name == '__init__':
                    continue

                name = 'bakery.ext.' + name
                print "   ", name, "...",

                e = load_dynamic(name, module)
                (imp, proc, exp) = e.extensions()
                importers.update(imp)
                processors.update(proc)
                exporters.update(exp)

                extensions[name] = e
                print "ok"
            except:
                print "error (not a module?)"

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
# - C99 helper library for extensions
# - Fully functional test extension (do something trivial with a text file)
# - Documentation for building extensions
# - Figure out how we'll generate runtime library
# - Generate runtime library
# - Core extensions

