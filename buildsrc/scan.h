#ifndef SCAN_H
#define SCAN_H

#include <string>
#include <vector>

/** Returns the name of each file (not directory) in the given directory
  * @param directory A path to the directory to list
  */
std::vector<std::string> listFiles(const std::string &directory);

/** Returns the name of each subdirectory in the given directory
  * @param directory A path to the directory to list
  */
std::vector<std::string> listSubdirs(const std::string &directory);

/** Returns the name of each file / subdirectory in the given directory
  * @param directory A path to the directory to list
  */
std::vector<std::string> listAll(const std::string &directory);

/** Recursively scans a directory for all files with a given extension
  * @param directory The root directory to scan, e.g. "./somedir"
  * @param extension The extension to search for, e.g. ".foo"
  * @return          The list of paths found, prefixed with {@param directory}
  *                  e.g. "./somedir/anotherdir/somefile.foo"
  */
std::vector<std::string> scan(const std::string &directory, 
                              const std::string &extension);

#endif
