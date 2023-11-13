from abc import ABC, abstractclassmethod
from io import TextIOWrapper

import csv

class CSVRepository(ABC):

    __csvFileReader: csv.reader
    __columns: list
    __data: list

    def __init__(self, data_file: TextIOWrapper) -> None:
        self.__data = []
        self.__csvFileReader = csv.reader(data_file)

        self.__columns = self.__getColumns()
        self.__mapData()
        data_file.close()
        

    def find(self, find_options = {}):
        res = []
        whereRes = []

        if find_options.get("where"):
            res = self.__processWhere(find_options["where"]) 

        else:
            res = self.__data
            
        
        if find_options.get('select'):
            res = self.__processSelect(res , find_options["select"]) 
        
        return res 

    def findBy(self, findby_options):
        return self.find({"where": findby_options}) 

    def countColumn(self, column) -> list:
        cafe_data = self.find({"select": [column]})
        cafe_set = set(map(lambda data: data[column], cafe_data))

        cafe_count = []
        for value in cafe_set:
            count = 0
            for cafe_value in cafe_data:
                if cafe_value[column] == value:
                    count += 1
            
            cafe_count.append({column: value, "count": count})
        
        return cafe_count

    def __processWhere(self, where_options) -> list:
        resWhereItem = []
        for row in self.__data:
                for where in where_options:
                    for key in where.keys():
                        if where[key] == row[key]:
                            resWhereItem.append(row)
        
        return resWhereItem

    def __processSelect(self, list_to_select, select_options) -> list:
        resSelectList = []
        for row in list_to_select:
                resItemDist = {}
                for select in select_options:
                    resItemDist[select] = row[select]
                
                resSelectList.append(resItemDist)
        
        return resSelectList

    def __getColumns(self) -> list:
        return self.__csvFileReader.__next__()

    def getColumns(self):
        return self.__columns

    def __mapData(self) -> None:
        for index, row in enumerate(self.__csvFileReader):
            dataRowDict = {}
            for i, column in enumerate(self.__columns):
                dataRowDict[column] = row[i]

            self.__data.append(dataRowDict)