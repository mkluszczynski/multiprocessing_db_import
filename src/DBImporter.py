# import os, sys, pathlib
# sys.path.append(str(pathlib.Path.cwd()))
from unidecode import unidecode
from lib.Repository.DBRepository import DBRepository
from lib.Repository.CSVRepository import CSVRepository

class DBImporter:

    __dbRepo: DBRepository

    def __init__(self, db_repo: DBRepository) -> None:
        self.__dbRepo = db_repo 

    def importDataFromCsvFile(self, file_path: str):
        csvFile = open(file_path)
        csvRepo = CSVRepository(csvFile)

        tableName = self.__trimToTableName(csvFile.name)

        data = csvRepo.find()
        self.__dbRepo.createTable(tableName, [self.__trimColumnName(column) for column in csvRepo.getColumns()])
        for row in data:
            rowList = self.__prepareInsertData(row)
            print(rowList)
            self.__dbRepo.add(
                    {
                        "insert": rowList,
                        "into": tableName
                    }
                )

    def __prepareInsertData(self, row: dict):
        return [{self.__trimColumnName(column): f"'{self.__replaceSpecialCharacters(value, ' ')}'"} for column, value in row.items() if column != ""]

    def __trimColumnName(self, columnName: str):
        return self.__replaceSpecialCharacters(columnName, "S")

    def __replaceSpecialCharacters(self, text: str, replace: str):
        banned = ["'", "%", "!", "?", "%", "@", "$", "^", "&", "-"]
        final = unidecode(text).replace(" ", "")
        for ban in banned:
            final = final.replace(ban, replace)

        return final 


    def __trimToTableName(self, file_path: str):
        return file_path.replace("data/", "").replace(".csv", "")

    



