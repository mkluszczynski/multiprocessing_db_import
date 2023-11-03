import sys
import time
from unidecode import unidecode
from colorama import Fore
from lib.Repository.DBRepository import DBRepository
from lib.Repository.CSVRepository import CSVRepository

class DBImporter:

    __dbRepo: DBRepository

    def __init__(self, db_repo: DBRepository) -> None:
        self.__dbRepo = db_repo 

    def importDataFromCsvFile(self, file_path: str):
        start = time.time()
        csvFile = open(file_path)
        csvRepo = CSVRepository(csvFile)

        tableName = self.__trimToTableName(csvFile.name)

        data = csvRepo.find()
        self.__dbRepo.createTable(tableName, [self.__trimColumnName(column) for column in csvRepo.getColumns()])
        print(f"{Fore.CYAN}Inserting {Fore.GREEN}{file_path} {Fore.CYAN}file...")
        insertedNo = 0
        for row in data:
            rowList = self.__prepareInsertData(row)
            self.__dbRepo.add(
                    {
                        "insert": rowList,
                        "into": tableName
                    }
                )
            insertedNo += 1
            self.__logInsertMessage(str(insertedNo), file_path, tableName)
            
        sys.stdout.write("\n")
        end = time.time()
        print(f"{Fore.CYAN}File {Fore.GREEN}{file_path} {Fore.CYAN}inserted in {Fore.MAGENTA}{int(end - start)}s")
            

        # print(f"{Fore.CYAN}Inserted data from {Fore.GREEN}{file_path} {Fore.CYAN}to {Fore.GREEN}{tableName} {Fore.CYAN}table.")
    def __logInsertMessage(self, value: str, file: str, table: str):
        sys.stdout.write(("\r{0} rows " + Fore.CYAN + "from " + Fore.GREEN + file + Fore.CYAN + " to " + Fore.GREEN + table + Fore.CYAN + " table.").format(f"{Fore.CYAN}Inserted {Fore.MAGENTA}" + value))
        sys.stdout.flush()

    def __prepareInsertData(self, row: dict):
        return [{self.__trimColumnName(column): f"'{self.__replaceSpecialCharacters(value, ' ')}'"} for column, value in row.items() if column != ""]

    def __trimColumnName(self, columnName: str):
        return self.__replaceSpecialCharacters(columnName, "S")

    def __replaceSpecialCharacters(self, text: str, replace: str):
        banned = ["'", '"', "%", "!", "?", "%", "@", "$", "^", "&", "-", "(", ")", "1", "."]
        final = unidecode(text).replace(" ", "")
        for ban in banned:
            final = final.replace(ban, replace)

        return final 


    def __trimToTableName(self, file_path: str):
        return self.__replaceSpecialCharacters(file_path.replace("data/", "").replace(".csv", ""), "")

    



