Bakery
======

Bakery is a system for importing and preprocessing game assets offline
(colloquially known as "baking"). 

## Why?

* Importing / preprocessing your assets at build time rather than
  runtime can drastically improve load times.

* Instead of compiling and distributing your content import libraries
  with your game, you only need to distribute Bakery's runtime library
  (which is lightweight, has no external dependencies, and is released
  under a permissive license). You'll still need to set up content
  import libraries, but only for your development environment. 

## How?

Bakery consists of an offline baking system (which may be run in batch
mode or integrated with other systems) and a thin, cross-platform 
runtime that imports baked content from byte streams. The former build
step creates baked assets that can be loaded in the latter step. 

In its default configuration, Bakery can handle

* Images (PNG, JPG, BMP, TIFF, TGA, others?)
* Text (sprite fonts, prerendered text)
* Audio (any format supported by [libavcodec](http://ffmpeg.org))
* Meshes (any format supported by [assimp](http://assimp.sourceforge.net))

Bakery is made available under the 
[BSD 3-Clause License](http://www.opensource.org/licenses/BSD-3-Clause).

## Bakery is in an early development stage

Things are likely to not work yet. Venture further at your own peril.

## Installation

Bakery's core has no dependencies other than the STL. However, Bakery is
distributed with a core set of plugins that support several formats. 
These plugins require the following libraries to be built in your
development environment (it's probably easiest to `make install` these,
assuming you're in a UNIX-like environment). 

* [libavcodec](http://ffmpeg.org)
* [assimp](http://assimp.sourceforge.net)

Once you're ready, you can build Bakery the unix way: 

    $ ./configure
    $ make -j 4

By default, Bakery creates the folder `bin/` containing the headers
and libraries needed to build content and load data at runtime. To
install these, run

    $ make install

## Baking Content

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

This process is described for each asset in a Bakefile, which can be 
executed to produce output via the command-line utility `bake`. 

For more detail on baking content, see `doc/baking.markdown`.

## Loading Content

Data is loaded directly from byte streams via `BakeryReader` objects. 
Bakery can automatically determine the correct `BakeryReader` for a given
byte stream. 

Once loaded, assets are considered immutable, and objects that use the
asset can point to the asset in memory.

Note Bakery does _not_ implement any sort of archive management or 
virtual filesystem. It can only load directly from byte streams.

For more detail on loading assets, see `doc/loading.markdown`. 

## Extensions

Bakery's plugin system makes it easy to modify the build chain for a file
type or create a new build chain for an entirely new type of file. 
For more information on installing or authoring extensions, see
`doc/extensions.markdown`.

