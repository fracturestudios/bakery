Bakery
======

**Note**: Bakery is still early in development.

Bakery is a system for importing and preprocessing game assets offline
(colloquially known as "baking"). 

Why? Because decoding and processing your assets at build time improves your
game's load times. And because it means not having to link your game against
asset libraries like assimp/avcodec. Or distribute them with your game. Or
cross-compile them if that's your thing.

Just set up those libraries once in your favorite development environment,
build the content once, and use it on any platform.

## How?

Bakery is a plugin-driven system in two movements:

The offline library imports and processes assets in their original formats.
It spits out a binary intermediate representation of the processed data.

The online library provides a thin, cross-platform library that reconstructs
the data from its intermediate representation.

The `bake` utility links against the offline library. It provides a simple
`Makefile`-like syntax for building content in batch mode.

In its default configuration, Bakery can handle

* Images (PNG, JPG, BMP, TIFF, TGA, others?)
* Text (sprite fonts, prerendered text)
* Audio (any format supported by [libavcodec](http://ffmpeg.org))
* Meshes (any format supported by [assimp](http://assimp.sourceforge.net))

Bakery is made available under the 
[BSD 3-Clause License](http://www.opensource.org/licenses/BSD-3-Clause).

## Installation

Bakery's core has no dependencies other than the STL. However, Bakery is
distributed with a core set of plugins that support several formats. 
These plugins require the following libraries to be in `g++`'s search
path:

* [libavcodec](http://ffmpeg.org)
* [assimp](http://assimp.sourceforge.net)

Once you're ready, you can build Bakery the unix way: 

    $ ./configure
    $ make -j 4
    $ make install

## Baking Content

Each asset is baked in three steps:

* In the _import_ step, the asset is decoded from its original file format.
* In the _processing_ step, zero or more transformations are applied to the
  asset's data. Each transformation can yield data in the same format or a
  different format.
* In the _writing_ step, the asset data is written to its binary intermediate
  representation.

For more about baking content, see `doc/baking.markdown`.

## Loading Content

Bakery's runtime loads the data produced by the offline system. Given a byte
array, the runtime determines the data's format and unpacks it into memory.

Bakery doesn't implement archive management or a virtual filesystem. To keep
the runtime small and cross-platform, it only supports loading directly from
byte streams.

For more about loading assets, see `doc/loading.markdown`. 

## Extensions

Bakery's plugin system makes it easy to modify the build chain for a file
type or create a new build chain for an entirely new type of file. 
For more information on installing or authoring extensions, see
`doc/extensions.markdown`.

