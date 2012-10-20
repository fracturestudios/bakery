
#include "manifest.h"

#include <cassert>
#include <fstream>
#include <sstream>

using namespace std;


static string objTypeStrs[] = 
{
    "<unknown>",
    "BAsset",
    "BImporter",
    "BProcessor",
    "BReader",
    "BWriter",
};

PluginManifestObjectType objTypeFromStr(const string &str)
{
    for (size_t i = 0; i < sizeof(objTypeStrs) / sizeof(objTypeStrs[0]); ++i)
        if (objTypeStrs[i] == str)
            return (PluginManifestObjectType)i;

    return OBJTYPE_UNKNOWN;
}

string objTypeToStr(PluginManifestObjectType type)
{
    return objTypeStrs[(size_t)type];
}


PluginManifestObject::PluginManifestObject() 
    : type(OBJTYPE_UNKNOWN)
{ }

PluginManifestObject::~PluginManifestObject() { }


PluginManifest::PluginManifest() { }

PluginManifest::~PluginManifest() { }

const string &PluginManifest::orgName() const
{
    return m_orgName;
}

void PluginManifest::setOrgName(const string &value)
{
    m_orgName = value;
}

const string &PluginManifest::pluginName() const
{
    return m_pluginName;
}

void PluginManifest::setPluginName(const string &value)
{
    m_pluginName = value;
}

const string &PluginManifest::pluginVersion() const
{
    return m_pluginVersion;
}

void PluginManifest::setPluginVersion(const string &value)
{
    m_pluginVersion = value;
}

const string &PluginManifest::includes() const
{
    return m_includes;
}

void PluginManifest::setIncludes(const string &value)
{
    m_includes = value;
}

const string &PluginManifest::libraries() const
{
    return m_libraries;
}

void PluginManifest::setLibraries(const string &value)
{
    m_libraries = value;
}

vector<PluginManifestObject> &PluginManifest::objects()
{
    return m_objects;
}

void PluginManifest::clear()
{
    m_orgName.clear();
    m_pluginName.clear();
    m_pluginVersion.clear();
    m_includes.clear();
    m_libraries.clear();
    m_objects.clear();
}

static inline bool isWhitespace(char c)
{
    return c == ' ' || c == '\t';
}

static inline void eatWhitespace(const string &line, size_t &i)
{
    for (; isWhitespace(line[i]); ++i)
        if (i == line.size())
            return;
}

static inline string nextToken(const string &line, size_t &i)
{
    string buf;

    for (; !isWhitespace(line[i]) && i < line.size(); ++i)
        buf += line[i];

    return buf;
}

static vector<string> tokenize(const string &line)
{
    vector<string> tokens;

    size_t i = 0;
    while (i < line.size())
    {
        // Eat whitespace before the token
        eatWhitespace(line, i);
        if (i == line.size())
            return tokens;

        // Read the token itself
        string token = nextToken(line, i);
        if (token.size() == 0)
        {
            assert(i == line.size());
            break;
        }

        // If it's a comment, we're done with this line
        if (token[0] == ';')
            break;

        // If it's an argument directive, take the rest of the line as the arg
        if (token == "INCLUDES" || token == "LIBRARIES")
        {
            tokens.push_back(token);

            eatWhitespace(line, i);

            if (i != tokens.size())
                tokens.push_back(line.substr(i));

            break;
        }

        tokens.push_back(token);
    }
    
    return tokens;
}

bool PluginManifest::load(const string &path)
{
    ifstream file(path.c_str(), ifstream::in);
    if (!file.good())
        return false;

    bool parsedHeader = false;

    string line;
    while (getline(file, line)) 
    {
        vector<string> tokens = tokenize(line);
        if (tokens.empty())
            continue;

        if (!parsedHeader) 
        {
            if (tokens.size() < 2)
            {
                // Invalid or missing header
                file.close();
                return false;
            }

            string name = tokens[0];
            if (name.find(".") == string::npos)
            {
                // Invalid plugin name (must be org.plugin)
                file.close();
                return false;
            }

            string version = tokens[1];
            if (version[0] != 'v')
            {
                // Invalid plugin version (must be vXYZ)
                file.close();
                return false;
            }

            m_orgName = name.substr(0, name.find("."));
            m_pluginName = name.substr(name.find(".") + 1);
            m_pluginVersion = version.substr(1);

            parsedHeader = true;
        } 
        else 
        {
            if (tokens[0] == "INCLUDES")
            {
                if (tokens.size() != 2)
                {
                    // Invalid INCLUDES directive
                    file.close();
                    return false;
                }

                m_includes = tokens[1];
            }
            else if (tokens[0] == "LIBRARIES")
            {
                if (tokens.size() != 2)
                {
                    // Invalid LIBRARIES directive
                    file.close();
                    return false;
                }

                m_libraries = tokens[1];
            }
            else
            {
                if (tokens.size() != 3)
                {
                    // Invalid exported object entry
                    file.close();
                    return false;
                }

                PluginManifestObject obj;
                obj.type = objTypeFromStr(tokens[0]);
                obj.name = tokens[1];
                obj.header = tokens[2];

                if (obj.type == OBJTYPE_UNKNOWN)
                {
                    // Invalid exported object type
                    file.close();
                    return false;
                }

                m_objects.push_back(obj);
            }
        }
    }

    file.close();
    return true;
}

bool PluginManifest::save(const string &path) const
{
    ofstream file(path.c_str(), ofstream::out | ofstream::trunc);
    if (!file.good())
        return false;

    file << m_orgName << "." << m_pluginName << " v" << m_pluginVersion << "\n";
    file << "INCLUDES " << m_includes << "\n";
    file << "LIBRARIES " << m_libraries << "\n";

    for (size_t i = 0; i < m_objects.size(); ++i)
    {
        const PluginManifestObject &o = m_objects[i];
        file << objTypeToStr(o.type) << " "
             << o.name << " "
             << o.header << "\n";
    }

    file.close();
    return true;
}

