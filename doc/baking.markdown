Baking Content
==============

Each asset is baked in three steps:

* First, the asset is _imported_. This step decodes the asset from its
  native format (e.g. .png, .ogg, .3ds) into an intermediate format.
  This step is completed by a `BakeryImporter`.

* Then, the asset is _processed_. Processors modify the input data in
  some way and produce an output, which may be of a different format.
  Processors form a chain where the input of each link is the same type
  as the ouptut of the previous link.
  This step is accomplished by a chain of `BakeryProcesor`s. 

* Finally, the asset is _written_ by a `BakeryWriter`. 

There are two ways to use Bakery

* If you have an existing build system, you can use the Bakery API to
  invoke the build chain for individual assets.
* Otherwise you can use the command-line utility `bake`.

## `bake`

`bake` is a batch-mode command line utility that feels like `make`. 
It processes directives in a `Bakefile`. 

A `Bakefile` consists of a list of directives, of the form

    output : input(s)
        recipe
        recipe
        recipe

* The `output` may be a folder to place baked assets in or a single
  file to output to. 
* The `input` may be one or more files to process
* The `recipe` lines tell Bakery how to process the file
    * The first line of a recipe is which `BakeryImporter` to use. 
      If no importer is specified, Bakery infers one based on the
      file extension of the input.
    * The rest of the lines are content processors that transform
      the loaded data. 
    * The last line denotes which `BakeryWriter` to use. If no
      writer is specified, Bakery infers one based on the type of
      the content produced by last importer / processor to run on
      the asset.

By default, `bake` reads the Bakefile in the current directory and
produces output in the current directory. Either can be changed 
using arguments to the command line utility.

The files produced by the baking step can then be loaded using
the Bakery runtime API. See `doc/loading.md`.

## Bakefiles by Example

To bake a single assset:

    menu/title : title.png

To process an asset:

    menu/title : title.png
        hueshift 120
        saturate 1.5

To process several files the same way:

    menu/ : title.png, controls.png
        hueshift 120
        saturate 1.5

In the above example, `bake` produces the output files `menu/title` and
`menu/controls`.

To specify how to import the image:

    menu/title : title.png
        MyImporter
        hueshift 120
        saturate 1.5

To specify how to write the image:

    menu/title : title.png
        MyImporter
        hueshift 120
        saturate 1.5
        MyWriter

To avoid redundancy, define recipes:

    menufx : theimage
        MyImporter
        hueshift 120
        saturate 1.5
        MyWriter

    menu/title : title.png
        menufx

## Bakery API

By example:

    #include "bakery/offline.h"

    bool process_img(const char *inpath, const char *outpath) {

        BImporter *imp = BImporter::infer(inpath);
        if (!imp)
            return false;

        BAsset *data = 0;
        int err = imp->import(inpath);
        if (err)
            return false;

        BProcessor *proc[] = { 
            my_get_hue_processor(),
            my_get_saturate_processor()
        };

        for (int i = 0; i < sizeof(proc) / sizeof(proc[0]); ++i) {
            err = proc[i]->process(&data);
            if (err) {
                delete data;
                return false;
            }
        }

        BWriter *writer = BWriter::infer(outpath);
        if (!writer) {
            delete data;
            return false;
        }

        err = writer->write(data, outpath);
        delete data;

        return (err == 0);
    }

