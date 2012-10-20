
#include <iostream>

#include "headers.h"
#include "makefile.h"
#include "manifest.h"

using namespace std;

static void printPlugins(const vector<PluginManifest> &manifests)
{
    for (size_t i = 0; i < manifests.size(); ++i)
    {
        const PluginManifest &pm = manifests[i];

        cout << "Loaded:  " << pm.path() << "\n"
             << "Plugin:  " << pm.pluginName() << "\n"
             << "By:      " << pm.orgName() << "\n"
             << "Version: " << pm.pluginVersion() << "\n"
             << "Include: " << pm.includes() << "\n"
             << "Libs:    " << pm.libraries() << "\n"
             << "Exports: \n";

        const vector<PluginManifestObject> obj = pm.objects();
        for (size_t j = 0; j < obj.size(); ++j)
        {
            const PluginManifestObject &o = obj[j];

            cout << "         " << o.name << " : public " << objTypeToStr(o.type)
                 << " [ " << o.header << " ] \n";
        }

        cout << "\n";
    }
}

static void genHeader(const string &inpath, 
                      const vector<PluginManifest> &manifests,
                      const string &outpath)
{
    cout << "Writing " << outpath << "...";
    cout.flush();

    Headers header;
    header.setBasePath(inpath);

    for (size_t i = 0; i < manifests.size(); ++i)
    {
        const vector<PluginManifestObject> &o = manifests[i].objects();

        for (size_t j = 0; j < o.size(); ++j)
            header.includePaths().push_back(o[i].header);
    }

    if (header.compile(outpath))
        cout << "done\n";
    else
        cout << "error\n";
}

static void genMakefile(const vector<PluginManifest> &manifests)
{
    cout << "Writing Makefile ...";
    cout.flush();

    cout << "not yet implemented\n";
}

int main(int argc, const char *argv[]) 
{
    vector<PluginManifest> manifests = PluginManifest::loadAll("./plugins");
        
    printPlugins(manifests);

    genHeader("src/bakery/offline.h", manifests, "include/bakery/offline.h");
    genHeader("src/bakery/runtime.h", manifests, "include/bakery/runtime.h");
    genMakefile(manifests);

    return 0;
}

