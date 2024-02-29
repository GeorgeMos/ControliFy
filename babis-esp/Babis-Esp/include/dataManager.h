#pragma once
#include <vector>

#ifndef __DATA_MANAGER__
#define __DATA_MANAGER__
class DataManager
{
    private:
    std::vector<int> _graphX;
    std::vector<int> _graphY;
    
    public:
    DataManager();
    void clearGraph();
    void appendGraph(int x, int y);
    int getMaxX();
    int getMaxY();
    int size();
    int getX(int i);
    int getY(int i);


};

#endif
