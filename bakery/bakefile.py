""" Utility for loading and saving build chains """

# TODO move all of this to a buildchain.py

class BuildStep:
    """ A step in the build chain """

    IMPORT  = 0 # A build step that produces an asset from a stream
    PROCESS = 1 # A build step that processes an asset
    EXPORT  = 2 # A build step that exports an asset to a stream

class BuildChain:

    inpath = ''
    importer = None
    outpath = ''
    exporter = None
    steps = [ ]

def _import_step(typename, filename):
    pass

def _process_step(typename, arglist):
    pass

def _export_step(typename, filename):
    pass

# TODO use buildchain.py here

def load(data):
    pass

def save(chain):
    pass

"""
def load_file(path):
    with open(path, 'r') as f
        return load(f.read())

def save_file(path):
    with open(path, 'w+') as f
        f.write(save(data))
"""

