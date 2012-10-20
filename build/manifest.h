#ifndef MANIFEST_H
#define MANIFEST_H

#include <string>
#include <vector>

/** Enumerates bakery base types an object exported in a 
  * bakery plugin can inherit from
  */
enum PluginManifestObjectType
{
    OBJTYPE_UNKNOWN,       // Trips an error at runtime
    OBJTYPE_BASSET,        // Inherits from BAsset
    OBJTYPE_BIMPORTER,     // Inherits from BImporter
    OBJTYPE_BPROCESSOR,    // Inherits from BProcessor
    OBJTYPE_BREADER,       // Inherits from BReader
    OBJTYPE_BWRITER,       // Inherits from BWriter
};

PluginManifestObjectType objTypeFromStr(const std::string &str);
std::string objTypeToStr(PluginManifestObjectType type);

/** An entry in a BakeryPlugin file, corresponding to a type the
  * plugin wishes to export to bakery's offline and runtime
  * libraries.
  */
class PluginManifestObject
{
public:
    PluginManifestObject();
    ~PluginManifestObject();

    /** The bakery type this entry's object inherits from */
    PluginManifestObjectType type;

    /** The fully qualified C++ type name of the object */
    std::string name;

    /** A path (relative to the plugin root) to the header 
      * defining this object 
      */
    std::string header;
};

/** Contains metadata about a BakeryPlugin object */
class PluginManifest
{
public:
    PluginManifest();
    ~PluginManifest();

    /** Gets or sets the path to the manifest file this object
      * corresponds to. If not applicable, returns an empty string.
      */
    const std::string &path() const;
    void setPath(const std::string &);

    /** Gets or sets the organization that created this plugin */
    const std::string &orgName() const;
    void setOrgName(const std::string &);

    /** Gets or sets the name of this plugin */
    const std::string &pluginName() const;
    void setPluginName(const std::string &);

    /** Gets or sets the version of this plugin */
    const std::string &pluginVersion() const;
    void setPluginVersion(const std::string &);

    /** Gets or sets the INCLUDES= line of the manifest */
    const std::string &includes() const;
    void setIncludes(const std::string &);

    /** Gets or sets the LIBRARIES= line of the manifest */
    const std::string &libraries() const;
    void setLibraries(const std::string &);

    /** Gets a reference to the manifest's list of objects
      * exported by this plugin.
      */
    std::vector<PluginManifestObject> &objects();
    const std::vector<PluginManifestObject> &objects() const;

    /** Removes all objects and resets all fields of this manifest */
    void clear();

    /** Clears this manifest and loads its contents from the file
      * at the given path. Not atomic -- the manifest will be cleared
      * even if the file cannot be parsed.
      */
    bool load(const std::string &path);

    /** Writes this manifest to the file at the given path, creating
      * or truncating it as necessary.
      */
    bool save(const std::string &path) const;

    /** Recursively scans a subdirectory for plugin manifests and loads them */
    static std::vector<PluginManifest> loadAll(const std::string &directory);

private:
    std::string                         m_path;
    std::string                         m_orgName;
    std::string                         m_pluginName;
    std::string                         m_pluginVersion;
    std::string                         m_includes;
    std::string                         m_libraries;
    std::vector<PluginManifestObject>   m_objects;
};

#endif
