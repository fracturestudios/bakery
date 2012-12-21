
bakery precompiles assets according to the steps defined in a build chain. A
build chain consists of:

* An import step
* Zero or more processing steps
* An export step

Per-asset build chains are specified using a Bakefile. Like make,
the bake utility searches the current directory for a Bakefile, parses it, and
builds any asset whose last-modified time is later than the precompiled
output's last-modified time.

## Syntax

Bakefiles superficially resemble Makefiles:

    output: input
        build steps

A full specification for an asset's build chain can be quite verbose:

    bin/assets/mymodel: assets/models/mymodel.3ds
        Import3dsModel(attributes=vertices,texcoords warn=all)
        GenerateNormals(output=normalmap)
        ExportModel(compress=none)

However, in many cases options can be omitted, to be replaced by sensible
defaults:

* Each build step can provide defaults for omitted options:

        bin/assets/mymodel: assets/models/mymodel.3ds
            Import3dsModel
            GenerateNormals
            ExportModel

* If the exporter is omitted, a suitable exporter will be chosen based on the
  type of the asset being precompiled:

        bin/assets/mymodel: assets/models/mymodel.3ds
            Import3dsModel
            GenerateNormals

* If the importer is omitted, a suitable importer will be chosen based on the
  input file's extension

        bin/assets/mymodel: assets/models/mymodel.3ds
            GenerateNormals

* If no processing steps are required, they can be omitted as well:

        bin/assets/mymodel: assets/models/mymodel.3ds

* If no output file path is provided, bakery will place the file in a folder
  called `build/`, alongside the top directory specified in the path:

        : assets/models/mymodel.3ds

  In the example above, the precompiled asset is saved to 
  `build/assets/models/mymodel.3ds.built`

Comments start at any instance of `#` and end a the end of the line.

## Dependencies

Some assets depend on multiple input files. For example, a model might depend
on its mesh, shaders, and textures. Bakefiles allow an output to have multiple
dependent inputs:

    output: input dependency dependency
        build steps
        build steps

The bake utility will rebuild the output file if the input or any dependency
has a last-modified time that is later than the output's last-modified time.
However, only the input will be imported into the build chain. Build steps can
choose to import sub-assets if necessary. This is simply done using bakery's
public API.

## Processing Multiple Files Identically

The output path can be generated using a Python regular expression. The syntax
for doing so is:

    output re=pattern: input
        build steps
        build steps

The final output path is obtained using 
[`re.sub`](http://docs.python.org/2/library/re.html). Specifically,

* `input` is passed as the `string` argument
* `output` is passed as the `repl` argument
* `pattern` is passed as the `pattern` argument

If the `re=` argument is omitted from the output path, the regular expression
`'^*$'` is used to match the entire input string, replacing it with the
specified output string. In this way, the output path is always a regular
expression.

There may be multiple input paths, specified by a widcard. The exact paths are
obtained by passing the input string through 
[`glob.glob`](http://docs.python.org/2/library/glob.html). Note that, if you
specify multiple globbed input paths, you should specify an output path with a
regular expression based on the input file name. Otherwise you'll end up
overwriting the single output file over and over, after processing each input
file, which isn't very useful.

Dependencies can be globbed too; however, the globbed dependency list will be
used for each globbed input. For example:

    output re=pattern: some/*/path some/*/dependency

will cause every output matching `some/*/path` to be rebuilt if any item
matching `some/*/dependency` has been modified since the last build.

## An Example

The following Bakefile demonstrates advanced concepts introduced earlier in
this article. Its purpose is to take a set of hi-res textured models and
produce low-res normal-mapped and textured models. Additionally, a game map 
which references these models will be compiled.

    # Create low-res assets from original high-res 3DS models
    # Regenerate if any model's mesh (.3ds), material (.mtl) or textures (.png) changed
    build/models/\1 re=assets/models/(*).3ds : assets/models/*.3ds, assets/models/*.mtl, assets/models/*.png
        Import3dsModel(attributes=all warn=all import-dependencies=all)
        NormalMap(decimate=0.25 normal-map-size=512x512)

    # Compile a map that references models from assets/models
    build/maps/rooftop: assets/maps/rooftop.map, assets/models/*
        MyMapImporter(mesh-search-dir=build/models)
        MyRadiositySolver
        MyShadowComputer

