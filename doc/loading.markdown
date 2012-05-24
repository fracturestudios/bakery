Loading Content
===============

Bakery loads data directly from user-provided byte streams. It does not
implement archive management or a virtual filesystem like 
[physicsfs](http://icculus.org/physfs/). 

To load baked content from your application, you need to link against
the Bakery runtime. The runtime is written in pure C++ with no external
dependencies, other than the STL. It works on many platforms without
requiring any modifications. 

## Loading Data

Loading the menu title image from the example in `doc/baking.md`:

    #include "bakery/runtime.h"

    BImage* load_img(const char *path) {

        void *buf; unsigned len;
        my_read_file(path, &buf, &len);

        BReader *read = BReader::for(buf, len);
        if (!read) 
            return 0;

        BImage *img = 0;
        if (0 != read->loadAs<BImage>(buf, len, &img))
            return 0;

        return img;
    }

A shorter, more convenient example:

    #include "bakery/runtime.h"

    BImage *load_img(const char *path) {

        void *buf; unsigned len;
        my_read_file(path, &buf, &len);

        BImage *img;
        if (0 != BReader::load<BImage>(buf, len, &img))
            return 0;

        return img;
    }

Loading an asset without yet knowing its type:

    #include "bakery/runtime.h"

    BAsset *load_something(const char *path) {

        void *buf; unsigned len;
        my_read_file(path, &buf, &len);

        BAsset *asset;
        if (0 != BReader::load(buf, len, &asset))
            return 0;

        return asset;
    }

Inspecting asset types at runtime:

    bool is_image(BAsset *asset) {
        return asset->type() == BImage::type();
    }

Bakery automatically detects if the input stream is not a Bakery asset, as
well as whether the type of the asset matches the type of the object being
loaded into. 

## Using Data

Every `BAsset` subtype works differently, exposing raw data and providing 
a few helper functions. Consult the documentation for each asset subtype
to learn how it works.

In general, Bakery assets should be treated immutably, so that all objects 
that refer to the same asset can share a pointer to the same data in memory. 
This removes pointer-ownership headaches and reduces memory waste from having 
several copies of the same asset in memory.

## Cleaning Up

Each `BAsset` has a `dispose()` function (and an `isDisposed()` function) that
frees the baking-store memory being used by the asset. `BAsset` destructors
normally call `dispose()`, so it can be considered safe to simply use the
`delete` keyword on an asset to free it.

