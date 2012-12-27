
from bakery.asset import *
from bakery.core import *

class BuildStep:
    """
    Represents an intermediate processing step in the build chain

    Attributes:

    name [str]      The name of the extension to call on this step
    args [dict]     Contains string key/value pairs to pass as parameters to
                    the extension at this step.
    """

    def __init__(self, name, args = { }):
        self.name = name
        self.args = args

    def __str__(self):
        ret = self.name + '('
        for (k, v) in self.args.items():
            ret += ' %s=%s' % (k, v)
        ret += ' )'
        return ret


class BuildChain:
    """
    Represents an entire build chain

    Attributes:

    import_step [BuildStep] How the asset is imported
    export_step [BuildStep] How the asset is exported
    process_steps [list]    The processing steps to apply to the asset,
                            in the order they should occur
    """

    def __init__(self, import_step = None, export_step = None):
        self._import_step = import_step
        self._export_step = export_step
        self._process_steps = [ ]

    def import_step(self, name, args = { }):
        """ 
        Sets the build chain's import step 

        name [str]  The name of the importer to use
        args [dict] Contains string key/value pairs to pass to the importer
        """

        self._import_step = BuildStep(name, args)

    def process_step(self, name, args = { }):
        """ 
        Sets the build chain's process step 

        name [str]  The name of the processor to use
        args [dict] Contains string key/value pairs to pass to the processor
        """
        self._process_steps.append(BuildStep(name, args))

    def export_step(self, name, args = { }):
        """ 
        Sets the build chain's export step 

        name [str]  The name of the exporter to use
        args [dict] Contains string key/value pairs to pass to the exporter
        """
        self._export_step = BuildStep(name, args)

    def bake(self, instream, outstream):
        """
        Executes the build chain

        instream [file]     An open binary file with the seek pointer at the
                            beginning. Contains the asset data to load.
        outstream [file]    An open binary file with the seek pointer at the
                            beginning. Receives the precompiled asset.
        """

        imp = self._import_step
        exp = self._export_step
        a = Asset()

        print '    ', str(imp)
        import_asset(instream, imp.name, imp.args, a)

        for p in self._process_steps:
            print '    ', str(p)
            process_asset(p.name, p.args, a)

        print '    ', str(exp)
        export_asset(outstream, exp.name, exp.args, a)

