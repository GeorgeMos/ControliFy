#Global imports
import time

#Local imports
from Communicator import udpCom


class esp32Driver():
    @staticmethod
    def sendGraph(com:udpCom, xData:list[float], yData:list[float]):
        com.send("GRAPH")
        for i in range(len(xData)):
            msg = "vals," + str(xData[i]) + "," + str(yData[i])
            #print(msg)
            com.send(msg)
            time.sleep(0.001)
        time.sleep(0.1)
        com.send("END")

    @staticmethod
    def sendLabelData(com:udpCom, xData:list[float], yData:list[float], pData:list[float]):
        com.send("GRAPH")
        for i in range(len(xData)):
            msg = "vals," + str(xData[i]) + "," + str(yData[i]) + "," + str(pData[i])
            com.send(msg)
            time.sleep(0.001)
        time.sleep(0.1)
        com.send("END")

    @staticmethod
    def recieveValues(com:udpCom) -> list[str]:
        try:
            message = com.recv()
            msgArr = message.split(",")
            #Parsing split message
            if(msgArr[0] == "vals"):
                val1 = msgArr[1]
                val2 = msgArr[2]
                values = [val1, val2]

                return values
            else:
                return ["-1", "-1"]
        except:
            return ["-1", "-1"]
        
        

    @staticmethod
    def run(com:udpCom):
        com.send("RUN")
        #com.send("RUN")