
from bakery.buildchain import *
from bakery.core import *

import glob
import re
import time

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

    def __init__(self, inputs = None, deps = None, outputs = None, \
                 pattern = None, chain = None):
        self.inputs = inputs
        self.deps = deps
        self.outputs = outputs
        self.pattern = pattern
        self.chain = chain if chain != None else BuildChain()

    def __str__(self):
        ret = '%s re=%s : %s' % (self.outputs, self.pattern, self.inputs)
        for dep in self.deps:
            ret += ', ' + dep
        ret += '\n'

        ret += '    %s\n' % str(self.chain._import_step)
        for step in self.chain._process_steps:
            ret += '    %s\n' % str(step)
        ret += '    %s\n' % str(self.chain._export_step)

        return ret

    def fill(self):
        """ Fills in any build steps missing from this item """
        # TODO
        # We need to do some designing here. Since assets can have multiple
        # channels, it's not clear which channel should be used in the default
        # exporter.
        # Furthermore, it's not even clear we need to have special behavior for
        # exporting. We could implement bakery.asset in C++ and have it do all
        # its own memory management. Then runtime wrapper just needs to know
        # how to load an asset. Users can fill out their structs by directly
        # using pointers created by the asset, e.g. by using a take() function.
        pass

    def _mtime(self, path):
        """ 
        Gets the given file's last modification time.
        Returns the unix epoch if the file does not exist.
        """
        try:
            return os.path.getmtime(path)
        except os.error:
            return 0

    def _epoch(self, paths):
        """
        Returns the most recent modification time for any file given by an item
        in the paths list. Any output file that was modified before the epoch
        needs to be rebuilt.
        """
        if len(paths) == 0:
            return 0

        return max([ self._mtime(p) for p in paths ])

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
        print # newline

        self.fill()

        inputpaths = glob.glob(self.inputs)

        if len(inputpaths) == 0:
            print 'WARNING - file(s) not found:', self.inputs
            print '          current working directory:', os.getcwd()

        deppaths = [ path for dep in self.deps for path in glob.glob(dep) ]

        depepoch = self._epoch(deppaths)

        for inpath in inputpaths:
            outpath = re.sub(self.pattern, self.outputs, inpath)

            intime = self._mtime(inpath)
            outtime = self._mtime(outpath)

            if outtime < intime or outtime < depepoch:
                print inpath, "-->", outpath

                instream = open(inpath, 'rb')
                outstream = open(outpath, 'wb+')

                self.chain.bake(instream, outstream)

                instream.close()
                outstream.close()


class Bakefile:
    """
    Represents, parses and processes an entire Bakefile

    Attributes:

    items [list]    A list of BakefileItem objects that populate the Bakefile
    """

    def __init__(self):
        self.items = [ ]

    def __str__(self):
        return '\n'.join([ str(i) for i in self.items ])

    def _parse(self, contents):
        """ Parses a bakefile and stores the result in this object """

        def refind(needle, haystack):
            """ Like str.find(), but matches a regex instead of a substring """
            m = re.search(needle, haystack)
            return m.start() if m else -1

        def partition(line, linenum):
            """ 
            Splits a string along ' ' boundaries, taking quotation marks into
            account. Uses '\"' as an escape character.

            Examples:

            'a'         => ['a']
            '  a    '   => ['a']
            'a b'       => ['a', 'b']
            '  a  b  '  => ['a', 'b']
            '"a b" c'   => ['a b', 'c']
            '"a b"c'    => ['a b', 'c']
            '\"a b\" c' => ['"a', 'b"', 'c']
            '"a b c'    => Exception: unterminated string constant
            """
            items = [ ]

            while len(line) > 0:
                line = line.strip()
                if line[0] == '"':  # quoted substring
                    end = refind('(?<!\\)"', line)
                    if end == -1:
                        raise Exception("Line %d: Unterminated string constant"
                                % (linenum + 1))
                    items.append(line[1:end])
                    line = line[end + 1:].strip()
                else:   # bare substring
                    end = line.find(' ')
                    if end > -1: # more after the space
                        items.append(line[:end])
                        line = line[end + 1:].strip()
                    else: # done!
                        items.append(line)
                        line = ''

            return items

        lines = contents.splitlines()

        # Strip comments
        for i in range(len(lines)):
            line = lines[i]
            idx = line.find('#')
            if idx > -1:
                line = line[:idx]
                lines[i] = line

        # Parse items until file is empty
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if len(line) == 0:
                i += 1
                continue

            # Non-empty line must be an item declaration

            # Split input and output clauses
            idx = line.find(':')
            if idx == -1:
                raise Exception("Line %d: Missing ':' in item" % (i + 1))

            outclause = line[:idx].strip()
            inclause = line[idx + 1:].strip()

            # Parse the output clause
            pattern = '(.*)'
            outputs = 'build/\\1.built'

            outparts = partition(outclause, i)
            if len(outparts) > 0:
                outputs = outparts[0]
            if len(outparts) > 1:
                pattern = outparts[1]
                if not pattern.startswith('re='):
                    raise Exception("Line %d: Expecting re= clause at %s"
                                     % (i + 1, outparts[1]))
                pattern = pattern[len('re='):]

            # Parse the input clause
            inparts = [ s.strip() for s in inclause.split(',')]
            if len(inparts) == 0:
                raise Exception("Line %d: No inputs for rule" % (i + 1))

            inputs = inparts[0]
            deps = inparts[1:]

            chain = [ ]

            # Parse build chain
            origline = i
            i += 1
            while i < len(lines) and                                \
                  len(lines[i].strip()) > 0 and                     \
                  (lines[i].startswith(' ') or lines[i].startswith('\t')):

                line = lines[i].strip()
                idx = line.find('(')
                if idx == -1:
                    if not is_extension(line):
                        raise Exception("Line %d: Unknown extension %s" \
                                        % (i + 1, line))

                    chain.append(BuildStep(line))
                else:
                    name = line[:idx]
                    if not is_extension(name):
                        raise Exception("Line %d: Unknown extension %s" \
                                        % (i + 1, name))

                    line = line[idx + 1:]

                    idx = line.find(')')
                    if idx == -1:
                        raise Exception("Line %d: Unmatched open-paren" % (i + 1))

                    argstr = line[:idx]
                    args = dict((a[:a.find('=')], a[a.find('=') + 1:]) \
                                for a in partition(argstr, i))

                    chain.append(BuildStep(name, args))
                i += 1

            # Construct item
            item = BakefileItem(inputs, deps, outputs, pattern)
            for step in chain:
                if step != chain[0] and is_importer(step.name):
                    raise Exception("With rule starting on line %d: importer %s must be first item in build chain" \
                                    % (origline + 1, step.name))
                elif step != chain[-1] and is_exporter(step.name):
                    raise Exception("With rule starting on line %d: exporter %s must be last item in build chain" \
                                    % (origline + 1, step.name))

                if is_importer(step.name):
                    item.chain._import_step = step
                elif is_exporter(step.name):
                    item.chain._export_step = step
                else:
                    item.chain._process_steps.append(step)

            self.items.append(item)

    def load(self, path):
        """ 
        Loads the contents of the bakefile at the given path, and stores its
        contents into this object
        """
        f = open(path, 'r')
        self._parse(f.read())
        f.close()

    def save(self, path):
        """ Writes the contents of this object into a Bakefile on disk """
        f = open(path, 'w')
        f.write(str(self))
        f.close()

    def bake(self):
        """ bake()s each item in the Bakefile """

        for i in self.items:
            i.bake()

