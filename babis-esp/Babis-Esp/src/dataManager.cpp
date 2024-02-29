#include "dataManager.h"


DataManager::DataManager()
{
    
}


void DataManager::clearGraph()
{
    this->_graphX.clear();
    this->_graphY.clear();
}

void DataManager::appendGraph(int x, int y)
{
    this->_graphX.push_back(x);
    this->_graphY.push_back(y);

}

int DataManager::getMaxX()
{
    int size = this->_graphX.size();
    int max = 0;
    for(int i = 0; i < size; i++){
        if(this->_graphX.at(i) >= max){
            max = this->_graphX.at(i);
        }
    }
    return max;
}

int DataManager::size()
{
    return this->_graphX.size();
}

int DataManager::getX(int i)
{
    return this->_graphX.at(i);
}

int DataManager::getY(int i)
{
    return this->_graphY.at(i);
}