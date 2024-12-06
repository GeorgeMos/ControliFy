from Communicator import udpCom
from DataManager import dataManager

class Handles:
    def __init__(self, comHandle:udpCom, dataHandle:dataManager):
        self.comHandle:udpCom = comHandle
        self.dataHandle:dataManager = dataHandle