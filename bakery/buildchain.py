
import bakery.core

class BuildStep:
    """
    Represents an intermediate processing step in the build chain

    Attributes:

    module [str]    The name of the module to defer to at this build step.
                    A value of 'Foo' means invoke bakery.ext.Foo
    args [dict]     The argument list to pass to the module. Argument names
                    map to argument values. Names and values are always
                    strings.
    """

    def __init__(self, module, args = { }):
        self.module = processor
        self.args = args
                            

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
        self.import_step = import_step
        self.export_step = export_step
        self.process_steps = [ ]

    def bake(self, instream, outstream):
        """ TODO uses high-level bakery.core api to import, process, export """
        pass

