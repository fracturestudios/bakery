Bakery Extensions
=================

At its core, Bakery is just infrastructure for precompiling content. Bakery's
plugins do all the heavy lifting. The core formats bakery supports are
implemented as a set of default plugins.

Every plugin is distributed as plain source. Bakery's build system 
automatically compiles every plugin's source into the Bakery headers
and libraries. 

## Compiling a Plugin into Bakery

The following diagram outlines the directory structure of the Bakery
repository and source code distribution:

    ./                      [repository root]
    |- configure            [first step of build process]
    |- include/             [bakery headers]
    |- bakesrc/             [source files for the bake utility]
    |- buildsrc/            [source files for the build system]
    |- src/                 [source files for runtime/offline libraries]
    \- plugins/             [plugin source, one directory per plugin]
       \- myplugin/         [contains the source for a plugin]
          |- myasset.h
          |- myasset.cpp
          |- myimporter.h
          |- ...
          \- BakeryPlugin   [contains metadata for Bakery's build system]

To add a plugin to bakery, you just need to drop its source folder into
`plugins/` and rerun the build process (`./configure && make -j 4 && 
make install`). The plugin may require external libraries: see the 
documentation for the specific plugin. 

## Authoring a Plugin

Most Bakery plugins either add a new processor to an existing build chain
or create a build chain for a new file format.

To add a processor, just implement `BProcessor`. This object will only
be available in the offline library, and therefore may use external libraries.

To create a build chain for a new format, you'll need to do the following:

* If you can't use an existing `BAsset` implementation for your content, 
  create a new one. If possible, it is highly recommended you reuse the core
  types available in the core plugin distribution.

  `BAsset`s are compiled into both the runtime and offline Bakery libraries.
  The runtime copy of the asset should not have external dependencies. To
  provide features that are only available for the offline library, use the
  `BAKERY_OFFLINE` and `BAKERY_RUNTIME` macros (which are `#define`d only 
  when building the offline and runtime libraries, respectively). 

* Implement a `BImporter` that reads files of the desired format and 
  produces the corresponding `BAsset` for processing. This object is only
  compiled into the offline library and may use external libraries. 

* Implement a `BWriter` that serializes your asset to an intermediate format.
  This format should be a tradeoff between matching your in-memory format (to
  provide fast load times) and ensuring the same file can be loaded on any
  platform. The `BWriter` object is only compiled into the offline library
  and may use external libraries.

* Implement a `BReader` that deserializes your asset into memory. This object
  is only compiled into the runtime libraries and should not use external
  libraries.

## Distribution

Bakery plugins are distributed as plain source files and are placed in the 
`plugins/` directory of the source tree before building. 

A custom build program is packaged with bakery. This program scans the
plugin directory for plugins and creates a pair of 'uber-headers' (`runtime.h`
and `offline.h`), consisting of the concatenation of all required plugin
headers. The script also registers all plugins with bakery.

In order for the build script to recognize your plugin, you must include a
`BakeryPlugin` file in the same directory as your plugin's source code.

### BakeryPlugin Files

BakeryPlugin files provide plugin metadata to the build system, allowing it
to integrate the plugin into Bakery's source code before compilation. The
file is structured as follows:

    OrganizationName.PluginName vVersionName
    ; This is a comment
    ; All empty lines are ignored

    TypeName ObjectName HeaderFile
    TypeName ObjectName HeaderFile
    TypeName ObjectName HeaderFile
    ...

* The first line describes the name and version of the plugin.
  Version numbers are freeform but should resemble an actual version number.
* Afterward there is one line for each object you need to register with 
  Bakery. Items are separated by arbitrary amounts of whitespace.
    * `TypeName` denotes which Bakery object type is implemented. Must be one of:
      `BAsset`, `BImporter`, `BProcessor`, `BWriter`, `BReader`.
    * `ObjectName` is the fully-qualified C++ object name. The build system uses
      this is to instantiate and register these objects.
    * `HeaderFile` is the name of the header file declaring this object. The
      build system uses this to include the headers in the appropriate uber-headers.

Example:

    FractureStudios.NullZeroLevel v1.0

    BAsset      NZLevel                     level.h
    BImporter   NZLevelImporter             importer.h
    BProcessor  NZLevelBSPBuilder           buildbsp.h 
    BProcessor  NZLevelLightmapCompiler     lightmaps.h
    BWriter     NZLevelWriter               writer.h
    BReader     NZLevelReader               reader.h

## Debugging

The Bakery offline API makes it easy to set up a test harness you can use to 
develop and debug your plugin. See `baking.markdown`.

