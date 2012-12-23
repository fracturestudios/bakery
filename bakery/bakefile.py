
from bakery.buildchain import *
from bakery.core import *

import re

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
                 pattern = None, chain = BuildChain()):
        self.chain = chain
        self.inputs = inputs
        self.deps = deps
        self.outputs = outputs
        self.pattern = pattern

    def _last_modified(self, path):
        return None # TODO

    def fill(self):
        """ Fills in any build steps missing from this item """
        pass

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

    def _parse(self, contents):
        """ TODO """

        def refind(needle, haystack):
            """ TODO """
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
                                % linenum)
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
                raise Exception("Line %d: Missing ':' in item" % i)

            outclause = line[:idx].strip()
            inclause = line[idx + 1:].strip()

            # Parse the output clause
            pattern = '(*)'
            outputs = 'build/\\1.built'

            outparts = partition(outclause, i)
            if len(outparts) > 0:
                outputs = outparts[0]
            if len(outparts) > 1:
                pattern = outparts[1]
                if not pattern.startswith('re='):
                    raise Exception("Line %d: Expecting re= clause at %s"
                                     % (i, outparts[1]))
                pattern = pattern[len('re='):]

            # Parse the input clause
            inparts = [ s.strip() for s in inclause.split(',')]
            if len(inparts) == 0:
                raise Exception("Line %d: No inputs for rule" % i)

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
                                        % (i, line))

                    chain.append(BuildStep(line))
                else:
                    name = line[:idx]
                    if not is_extension(name):
                        raise Exception("Line %d: Unknown extension %s" \
                                        % (i, name))

                    line = line[idx + 1:]

                    idx = line.find(')')
                    if idx == -1:
                        raise Exception("Line %d: Unmatched open-paren" % i)

                    argstr = line[:idx]
                    args = dict((a[:a.find('=')], a[a.find('=') + 1:]) \
                                for a in partition(argstr))

                    chain.append(BuildStep(name, args))
                i += 1

            # Construct item
            item = BakefileItem(inputs, deps, outputs, pattern)
            for step in chain:
                if step != chain[0] and is_importer(step.name):
                    raise Exception("With rule starting on line %d: importer %s must be first item in build chain" \
                                    % (origline, step.name))
                elif step != chain[-1] and is_exporter(step.name):
                    raise Exception("With rule starting on line %d: exporter %s must be last item in build chain" \
                                    % (origline, step.name))

                if is_importer(step.name):
                    item.chain._import_step = step
                elif is_exporter(step.name):
                    item.chain._export_step = step
                else:
                    item.chain._process_steps.append(step)

            self.items.append(item)

    def load(self, path):
        """ TODO """

        f = open(path, 'r')
        self._parse(f.read())
        f.close()

    def save(self, path):
        pass

    def bake(self):
        """ bake()s each item in the Bakefile """

        for i in self.items:
            i.bake()

