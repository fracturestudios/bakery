Bakery
======

Bakery is a system for importing and preprocessing game assets offline
(colloquially known as "baking"). There are several benefits to
baking your game's content:

* You no longer need to compile and distribute your content import
  libraries (e.g. [assimp](http://assimp.sourceforge.net), 
  [libpng](http://www.libpng.org/pub/png/libpng.html)) for every platform
  your game supports. Instead, you need only set up these libraries on
  your development machine. 

* By preprocessing your data once at build time, you can reduce the
  work your game does at runtime, decreasing loading wait time.

Bakery consists of an offline baking system (which may be run in batch
mode or integrated with other systems) and a thin, cross-platform 
runtime that imports baked content from byte streams.

In its default configuration, Bakery can handle

* Images (PNG, JPG, BMP, TIFF, TGA, others?)
* Audio (any format supported by [libavcodec](http://ffmpeg.org))
* Meshes (any format supported by [assimp](http://assimp.sourceforge.net))

Bakery is made available under the 
[LGPL v3](http://www.opensource.org/licenses/lgpl-3.0.html).

### Bakery is in an early development stage

Move along now ...

### Using Bakery

### Extending Bakery

