Bakery
======

Bakery is a system for importing and preprocessing game assets offline
(colloquially known as "baking"). 

### Why?

* You no longer need to compile and distribute your content import
  libraries (e.g. [assimp](http://assimp.sourceforge.net), 
  [libpng](http://www.libpng.org/pub/png/libpng.html)) for every platform
  your game supports. Instead, you need only set up these libraries for
  your development environment.

* By preprocessing your data once at build time, you can reduce the
  work your game does at runtime, decreasing loading wait time.

### How?

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
[LGPL v3](http://www.opensource.org/licenses/lgpl-3.0.html).

### Bakery is in an early development stage

Move along now ...

### Baking Content

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

For more detail on baking content, see `doc/baking.md`.

### Loading Content

Data is loaded directly from byte streams via `BakeryReader` objects. 
Bakery can automatically determine the correct `BakeryReader` for a given
byte stream. 

Once loaded, assets are considered immutable, and objects that use the
asset can point to the asset in memory.

Note Bakery does _not_ implement any sort of archive management or 
virtual filesystem. It can only load directly from byte streams.

For more detail on loading assets, see `doc/loading.md`. 

### Extending Bakery

Bakery's plugin system allows you to author build chains for new file types,
taking advantage of existing infrastructure. For information on doing so,
consult `doc/authoring.md`.

