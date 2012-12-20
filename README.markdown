
bakery will be an asset precompiler for game developers. Offline preprocessing
provides developers with two major developers:

* Since most of the heavy lifting is done once, offline, load times may improve
* Since only the precompiler needs to import assets from their 'native'
  formats (e.g. .3ds, .png, .mp3), only the precompiler needs to link against
  specialized libraries for doing so (e.g. assimp, avcodec). This makes
  compiling cross-platform a bit less of a headache!

## How It Works

Bakery consists of two pieces: an extensible offline precompiler, written in
Python, and an online runtime, written in pure (no-dependency) C++. The
precompiler produces raw asset files, which the runtime can parse and load.
Assets are generally stored in a raw binary format that allows the game to load
the object by memcpying C++ objects.

Extensions can extend the pipeline by

* Adding a new intermediate asset type
* Importing from a new format
* Creating a preprocessing step as part of the build chain

## Setting Up

How can you set up something that doesn't exist? #zen

