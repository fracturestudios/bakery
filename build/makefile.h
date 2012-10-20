#ifndef MAKEFILE_H
#define MAKEFILE_H

#include <string>
#include <vector>

/** Generates a Makefile to build bakery's offline and runtime pipelines */
class Makefile
{
public:

private:
};

/* TODO
 *
 * Configuration parameters
 * - Includes to copy to the include directory
 *      Should contain includes in src/bakery that aren't offline.h / runtime.h
 *      Should contain includes from each plugin, prefix with plugin name?
 *          If we do that, maybe the uber-header should #include, not embed
 * - Per-binary
 *      - Type (binary or lib)
 *      - Output directory
 *      - Target                $(TARGET)
 *      - Include flags         $(INCLUDES)
 *      - Lib flags             $(LIBS)
 *      - Header list           $(HEADERS)
 *      - Source list           $(SOURCES)
 *      - Cflags                $(CFLAGS)
 *      - Ldflags               $(LDFLAGS)
 * - Parameters for make install
 *      - Prefix
 *      - Targets
 * - Directories to confclean
 * - Should we support version numbers on the binaries we create?
 *
 * Generate by
 *  - Generating per binary lists from the parameters
 *  - Generating copy lists
 *  - Rules to build each target
 *  - Plumbing rules for building %.cpp -> %.o
 *  - Rules to copy files to destinations
 *  - all rule to copy files and build every target
 *  - install rule to copy each built target to the correct prefix dir
 *  - clean rule for deleting intermediate .o files
 *  - confclean rule for deleting dirs created by the configure script
 *  - distclean rule that does clean / confclean / deletes binaries, Makefile
 */

#endif
