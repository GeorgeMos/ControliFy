import csv


class dataManager:
    def __init__(self):
        self.files = [] #Array holding all imported csv files

    def addFile(self, filename):
        self.files.append(csvFile(filename))
        



class csvFile:
    def __init__(self, fileName:str):
        self.fileName = fileName
        self.xData = []
        self.yData = []
        self.openFile()

    def openFile(self):
        with open(self.fileName, newline='') as csvfile:
            fileRead = csv.reader(csvfile, delimiter=',', quotechar='|')

            for row in fileRead:
                print(', '.join(row))