
#include "headers.h"

#include <fstream>

using namespace std;

string HEADERS_DIRECTIVE("// %%BAKERY_PLUGINS%%");

Headers::Headers() { }

Headers::~Headers() { }

const string &Headers::basePath() const
{
    return m_basePath;
}

void Headers::setBasePath(const string &value)
{
    m_basePath = value;
}

const vector<string> &Headers::includePaths() const
{
    return m_includePaths;
}

vector<string> &Headers::includePaths()
{
    return m_includePaths;
}

string read(const string &path)
{
    ifstream file(path.c_str(), ifstream::in);
    if (!file.good())
        return "";

    string content((istreambuf_iterator<char>(file)),
                   istreambuf_iterator<char>());

    file.close();
    return content;
}

string concatAll(const vector<string> &paths)
{
    string content;

    for (size_t i = 0; i < paths.size(); ++i)
        content += read(paths[i]) + "\n";

    return content;
}

bool Headers::compile(const string &destPath)
{
    string includes = concatAll(m_includePaths);
    
    ifstream in(m_basePath.c_str(), ifstream::in);
    if (!in.good())
        return false;

    ofstream out(destPath.c_str(), ifstream::out | ifstream::trunc);
    if (!out.good())
    {
        in.close();
        return false;
    }

    string line;
    while (getline(in, line))
    {
        if (line == HEADERS_DIRECTIVE)
            out << includes << "\n";
        else
            out << line << "\n";
    }

    in.close();
    out.close();
    return true;
}

