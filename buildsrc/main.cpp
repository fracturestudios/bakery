
#include <iostream>

#include "scan.h"

int main(int argc, const char *argv[]) 
{
    std::vector<std::string> cpps = scan("..", ".cpp");
    for (size_t i = 0; i < cpps.size(); ++i)
        std::cout << cpps[i] << "\n";

    return 0;
}

