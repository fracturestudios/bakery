Bakery Extensions
=================

## TODO - The Current Plan

Every plugin is distributed in plain source, and contains two components:

* The runtime component contains definitions for `BAsset` and 
  `BReader` subtypes. This component should be entirely self-contained,
  i.e. no external dependencies (if it can be helped) beyond the STL.

* The offline component contains definitions for `BWriter`, `BProcessor`,
  and/or `BImporter` subtypes. This component may rely on external 
  libraries, especially for importing files from their native formats. 

The source code for Bakery includes a `plugins/` directory, into which 
plugins can be copied. The build system automatically includes the plugin
source code when compiling the offline and runtime libraries. 

## TODO - Things to figure out

* Still need to register BImporter / etc implementations at runtime
* Need a typing system that uniquely identifies asset types without
  needing to worry about collisions.
* How exactly do we lay out the plugins directory? How do we compile 
  everything together? 
* How can we possibly debug this if an extension starts acting up?
* Does this require us to use a permissive license for everything?

