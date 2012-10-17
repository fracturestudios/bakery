Baking Content
==============

Each asset is baked in three steps:

* First, the asset is _imported_. This step decodes the asset from its native 
  format (e.g. .png, .ogg, .3ds) into an intermediate format. This step is 
  completed by a `BakeryImporter`.
* Then, the asset is _processed_. Processors modify the asset data in a
  meaningful way. The output can be data in the same or a different format.
* Finally, the asset is _written_ by a `BakeryWriter`. 

The overall pipeline forms a chain, starting with a `BakeryImporter` and 
ending with a `BakeryWriter`. There can be zero or more `BakeryProcessor`s
in between. The output format of each link in this chain is always the same
as the input format of the next link.

There are two ways to use Bakery

* If you have an existing build system, you can use the Bakery API to
  invoke the build chain for individual assets.
* Otherwise you might find it simpler to use the `bake` utility.

## `bake`

`bake` is a batch-mode command line utility that feels like `make`. 
It processes directives in a `Bakefile`. 

A `Bakefile` consists of a list of directives, of the form

    output_path: importer(input_path)
        processor
        processor(args)
        writer

* `output_path` is the file to write the final output to. If the path contains
  spaces or commas, it should be enclosed in double quotes.
* `input_path` is the file to read initially. If the path contains spaces or 
  commas, it should be enclosed in double quotes.
* `importer` is the importer to use to read the file. If you would like bakery
  to infer the proper importer from the file's path, you can just specify the
  file path without an importer.
* `processor` directives consist of the name of a processor, plus any optional
  arguments to pass to the processor. Processor direectives are processed from 
  top to bottom (i.e. in the order specified).
* `writer` is the name of the `BakeryWriter` to use to finally serialize the
  asset. If no writer is specified, bakery will use the writer paired with the
  selected importer, if available. 

By default, `bake` reads the Bakefile in the current directory and
produces output in the current directory. Either can be changed 
using arguments to the command line utility.

The files produced by the baking step can then be loaded using
the Bakery runtime API. See `doc/loading.markdown`.

## Bakefiles by Example

To bake a single assset:

    menu/title : title.png

To process an asset:

    menu/title : title.png
        HueShift(120)
        Saturate(1.5)

To specify how to import the image:

    menu/title : MyPngImporter(title.png)
        HueShift(120)
        Saturate(1.5)

To additionally specify how to write the image:

    menu/title : MyPngImporter(title.png)
        HueShift(120)
        Saturate(1.5)
        MyPngExporter

## Bakery API

By example:

    #include "bakery/offline.h"

    bool bakeImage(const char *inpath, const char *outpath) 
    {
        BImporter *imp = BImporter::infer(inpath);
        if (!imp) {
            return false;
        }

        BAsset *data = 0;
        int err = imp->import(inpath);
        if (err) {
            return false;
        }

        BProcessor *proc[] = { 
            getMyHueProcessor(120),
            getMySaturateProcessor(1.5),
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

