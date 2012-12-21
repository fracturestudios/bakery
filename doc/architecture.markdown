
Bakery is an extension-driven tool for precompiling game assets. It assumes
that you want to encode your assets into a format that is readily accessible
for games, written in C or C++. However, you may use any language that can call
into C bindings, since bakery exposes a simple C API. C was chosen because it
is a lowest common denominator, as well as the platform many games are still
developed on. It is also the language in which many libraries for importing
content are written in.

There are two separate but cooperative pieces of bakery. The first is the
offline system, which imports content files in their original formats (e.g.
.3ds, .png, .mp3), does some sort of processing, and saves them to an
uncompressed binary format that can be loaded extremely quickly. The second
part is the runtime library, which loads the assets saved from the offline
step. The runtime is written in standard C99 with no dependencies other than
the C standard library. This is done to alleviate the headaches of compiling
asset importer libraries across every release platform.

Content comes in all shapes and sizes, from standardized and well-known formats
(like .png or .mp3) to custom home-brewed formats. It's thus important for
bakery to be highly extensible. At the end of the day, bakery provides some
unified glue around complex plugins that hook into well-known content-loading
libraries. Much of the effort behind bakery has been spent developing
reasonable conventions for the extensions to conform to.

## Offline

The offline system is written in Python. Python was chosen for its relative
ubiquity, the ease of loading dynamic extensions, and the relative ease of
integrating C bindings with Python.

### Asset Packaging

Bakery provides a container class (`bakery.asset.Asset`) that can hold multiple
related pieces of content that form a single asset. An Asset is the
intermediate representation of an object that is moving through a bakery build
pipeline.

The asset consists of 

* A list of byte buffers, which are allocated in C and opaque to the Python
  runtime. Management of this memory is performed by extensions.

* A one-to-one mapping from ID string to byte buffer. Each ID string uniquely
  identifies one of the byte buffers by name. Typically these ID strings signify 
  what type of data is stored in the byte buffer. Common examples include 
  `vertices`, `indexbuffer`, `texture0`.

* A one-to-many mapping from type ID string to byte buffer. Each type ID string
  specifies the type of data in each byte buffer. Type IDs are established by
  convention. Some common type IDs are `vertex_pos_norm_texcoord`,
  `image_r8g8b8a8`, `wav_441kHz_16bit_2ch`.

Extensions can store and retrieve an asset's byte buffers. An exception is
thrown (and baking is cancelled) when a requested byte buffer can't be found.
This usually indicates a bug in the extension or (more likely) a build chain
misconfiguration.

### `core` Module

As the lowest level, core is responsible for interacting with extensions. Core
finds and loads bakery extensions, and provides an interface for performing
build steps by calling into the extensions.

### `buildchain` Module

buildchain is built directly on top of core. Whereas core provides entry points
into the extensions, buildchain provides an interface for constructing a chain 
of build steps that

* Starts with an import step
* Follows up with zero or more processing steps
* Finishes with an export step

A build chain can be executed on input and output streams to completely build
an asset.

### `bakefile` Module

bakefile is built directly on top of buildchain. It parses and processes
directives found in a Bakefile. For more information on bakefiles, see
`doc/bakefile.markdown`

### Extensions

Extensions are compiled into dynamic libraries that can be loaded as Python
modules. The only requirement on the modules themselves is the presence of a
module-level function called `extensions()`, which returns a 3-tuple 
`(importers, processors, exporters)`. 

### `importers`

This item is a dictionary containing callbacks that can be used to load assets
from their original formats. The dictionary maps from `name` to
`(file_extensions, callback)`.

* `name` is the name of the importer. This is the string that ends up in the
  build steps of a Bakefile (see `docs/bakefile.markdown`)

* `file_extensions` is a list of file extensions this plugin can handle. Each
  extension should be a string consisting of the extension without the leading
  '.' (i.e. `png` not `.png`)

`callback` is a function, 

    callback(stream, args, asset)

* `stream` - A file object opened to the asset to be processed, with the seek
             pointer at the start of the file. Ready to be read.
* `args` - A dictionary of key/value string pairs containing arguments
           specified by the user, usually through a Bakefile
* `asset` - A container for loaded data. See the Asset Packaging section.

The function doesn't return anything. If it fails, it raises an exception.

### `processors`

This item is a dictionary containing callbacks that can be used to do some
processing on assets that have been loaded already. The dictionary maps from
`name` to a `callback` function. `name` is defined the same as in the 
`importers` section above. The callback function has the signature

    callback(asset, args)

* `asset` - A bakery asset container that contains the loaded data to process
            and should receive the processed data
* `args` - A dictionary of key/value string pairs containing arguments
           specified by the user, usually through a Bakefile

The function doesn't return anything. If it fails, it raises an exception.

### `exporters`

This item is a dictionary containing callbacks that can be used to write assets
to a file. The dictionary maps from `name` to a `callback` function. `name` is
defined the same as in the `importers` section above. The callback function has
the signature

    callback(asset, args, stream)

* `asset` - A bakery asset container that contains the data to export
* `args` - A dictionary of key/value string pairs containing arguments
           specified by the user, usually through a Bakefile
* `stream` - A file object, opened in binary mode, to which binary asset data
             should be written.

The function doesn't return anything. If it fails, it raises an exception.

## TODO Runtime

How are we going to generate the runtime sources? I feel like we're going to
need to ask the extension for a list of files to copy

We should use "loader" as the terminology for things that load exported
assets

