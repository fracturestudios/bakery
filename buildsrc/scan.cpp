
#include "scan.h"

#ifndef _WIN32
#include <dirent.h>
#else
#endif

using namespace std;

static vector<string> listNative(const string &directory,
                                 bool allowFiles,
                                 bool allowDirectories)
{
    vector<string> contents;

#ifndef _WIN32
    static const char *omit[] = { ".", ".." };
    struct dirent *ent = 0;

    DIR *dir = opendir(directory.c_str());
    if (!dir)
        return contents;

    while ((ent = readdir(dir))) {
        bool omitted = false;

        for (size_t i = 0; i < sizeof(omit) / sizeof(omit[0]); ++i) {
            if (0 == strcmp(ent->d_name, omit[i])) {
                omitted = true;
                break;
            }
        }

        bool isDir = ent->d_type & DT_DIR;

        if ((isDir && !allowDirectories) || (!isDir && !allowFiles))
            omitted = true;

        if (!omitted)
            contents.push_back(ent->d_name);
    }

    closedir(dir);
#else
#endif

    return contents;
}

vector<string> listFiles(const string &directory)
{
    return listNative(directory, true, false);
}

vector<string> listSubdirs(const string &directory)
{
    return listNative(directory, false, true);
}

vector<string> listAll(const string &directory)
{
    return listNative(directory, true, true);
}

static bool endsWith(const string &base, const string &suffix)
{
    if (base.size() < suffix.size())
        return false;

    string chopped = base.substr(base.length() - suffix.length());
    return 0 == chopped.compare(suffix);
}

static void scanRecursive(const string &directory,
                          const string &extension,
                          vector<string> &out)
{
    // Find files in this directory
    vector<string> files = listFiles(directory);

    if (files.size() > 0) {
        for (int i = (int)files.size() - 1; i >= 0; --i) {
            if (!endsWith(files[i], extension))
                files.erase(files.begin() + i);
        }

        for (size_t i = 0; i < files.size(); ++i) 
            out.push_back(directory + "/" + files[i]);
    }

    // Recur on subdirectories
    vector<string> subdirs = listSubdirs(directory);
    for (size_t i = 0; i < subdirs.size(); ++i)
        scanRecursive(directory + "/" + subdirs[i], extension, out);
}

vector<string> scan(const string &directory, const string &extension)
{
    vector<string> out;
    scanRecursive(directory, extension, out);

    return out;
}

