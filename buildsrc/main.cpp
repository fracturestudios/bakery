
#include <iostream>

#include "manifest.h"
#include "scan.h"

using namespace std;

int main(int argc, const char *argv[]) 
{
    vector<string> manifests = scan("plugins", "BakeryPlugin");
    for (size_t i = 0; i < manifests.size(); ++i)
    {
        PluginManifest pm;
        if (!pm.load(manifests[i]))
        {
            cout << "Warning: couldn't parse " << manifests[i] << "\n";
            continue;
        }

        cout << "Loaded:  " << manifests[i] << "\n"
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

    return 0;
}

