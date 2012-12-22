
import bakery.asset

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
    """ Search for extensions in _EXTROOT and loads them """

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

def all_importers():
    """ Gets the name of every loaded importer extension """
    return importers.keys()

def all_processors():
    """ Gets the name of every loaded processor extension """
    return processors.keys()

def all_exporters():
    """ Gets the name of every loaded exporter extension """
    return exporters.keys()

def default_importer(path):
    """ Gets the name of the default importer for the given file path """

    ext = os.path.splitext(path)[1]
    ext = ext[1:] # remove leading '.'

    global importers
    for name in importers:
        exts = importers[name][0]
        if ext in exts:
            return name

    return None

def importer(name):
    """ Gets the callback for the importer with the given name """
    return importers[name][1]

def processor(name):
    """ Gets the callback for the processor with the given name """
    return processors[name]

def exporter(name):
    """ Gets the callback for the exporter with the given name """
    return exporters[name]

def import_asset(stream, importer, args, asset):
    """
    Imports an asset by calling into an extension. If the importer fails for
    some reason, an exception is thrown. No value is returned.

    stream [file]   A file, opened in binary mode, with the seek pointer at the
                    beginning. Contains the binary data that should be
                    imported.
    importer [str]  The name of the importer extension to use
    args [dict]     A dictionary of string key/value pairs to pass to the
                    importer
    asset [Asset]   The bakery asset that will receive the loaded data.
    """

    cb = importers[importer][1]
    cb(stream, args, asset)

def process_asset(processor, args, asset):
    """
    Processes an asset by calling into an extension. If the processor fails for
    some reason, an exception is thrown. No value is returned.

    processor [str] The name of the processor extension to use
    args [dict]     A dictionary of string key/value pairs to pass to the
                    processor
    asset [Asset]   The bakery asset containing the data to process. Processed
                    data will be stored in the same asset.
    """

    cb = processors[processor]
    cb(args, asset)

def export_asset(stream, exporter, args, asset):
    """
    Exports an asset by calling into an extension. If the exporter fails for
    some reason, an exception is thrown. No value is returned.

    stream [file]   A file, opened in binary mode, with the seek pointer at the
                    beginning. Receives the exported binary data.
    exporter [str]  The name of the exporter extension to use
    args [dict]     A dictionary of string key/value pairs to pass to the
                    exporter
    asset [Asset]   The bakery asset containing the data to export
    """

    cb = exporters[exporter]
    cb(stream, args, asset)

# TODO
# - buildchain module
# - bakefile module
# - C99 helper library for extensions
# - Fully functional test extension (do something trivial with a text file)
# - Documentation for building extensions
# - Figure out how we'll generate runtime library
# - Generate runtime library
# - Core extensions

