
import bakery.buildchain
import bakery.core

class BakefileItem:
    """
    Represents a directive in a bakefile. A directive is a complete clause of
    the form,

    output re=pattern: input, dependencies
        build steps

    Attributes:

    chain [BuildChain]  The input/process/output steps for each asset
    inputs [str]        A glob string selecting all inputs to this item
    deps [list]         A list of glob strings selecting all inputs on which
                        this asset depends
    outputs [str]       A re.sub replacement string specifying the output for
                        each globbed input
    pattern [str]       A re.sub search string selecting arguments for the
                        output string
    """

    def __init__(self):
        self.chain = None
        self.inputs = None
        self.deps = None
        self.outputs = None
        self.pattern = None

    def _last_modified(self, path):
        return None # TODO

    def bake(self):
        """
        Processes this directive

        All inputs and dependencies are first globbed. For each input path, the
        corresponding output path is computed using re.sub().

        For each input/output pair, the output's last-modified time is checked
        against that of the input and every dependency. If the output doesn't
        exist or is out of date, the input is loaded and passed through the
        build chain using the API in bakery.core.
        """
        pass


class Bakefile:
    """
    Represents, parses and processes an entire Bakefile

    Attributes:

    items [list]    A list of BakefileItem objects that populate the Bakefile
    """

    def __init__(self):
        self.items = [ ]

    def load(self, path):
        pass

    def save(self, path):
        pass

    def bake(self):
        """ bake()s each item in the Bakefile """

        for i in self.items:
            i.bake()

