#ifndef HEADERS_H
#define HEADERS_H

#include <string>
#include <vector>

#include "manifest.h"

extern std::string HEADERS_DIRECTIVE;

/** Aggregates and concatenates headers */
class Headers
{
public:
    Headers();
    ~Headers();

    /** Gets or sets the path to the template header, into which
      * the include headers will be directly embeeded in the next
      * call to Headers::compile().
      *
      * The template header must contain a line matching
      * HEADERS_DIRECTIVE (see above).
      */
    const std::string &basePath() const;
    void setBasePath(const std::string &);

    /** Gets or sets a list of paths to headers to embed into
      * the final header during the next call to Headers::compile().
      */
    const std::vector<std::string> &includePaths() const;
    std::vector<std::string> &includePaths();

    /** Creates an uber-header by directly embedding all the headers
      * in includePaths() into the template at basePath().
      */
    bool compile(const std::string &destPath);

private:
    std::string                 m_basePath;
    std::vector<std::string>    m_includePaths;
};

#endif
