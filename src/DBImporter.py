import sys
import time
from unidecode import unidecode
from colorama import Fore
from lib.Repository.DBRepository import DBRepository
from lib.Repository.CSVRepository import CSVRepository

class DBImporter:

    __dbRepo: DBRepository
    __table_name: str
    __file_path: str
    __should_log: bool
    __csv_repo: CSVRepository

    def __init__(self, db_repo: DBRepository, table_name: str, file_path: str, shoudl_log: bool = False) -> None:
        self.__dbRepo = db_repo 
        self.__table_name = self.__trimToTableName(table_name)
        self.__file_path = file_path
        self.__should_log = shoudl_log
        csvFile = open(self.__file_path)
        self.__csv_repo = CSVRepository(csvFile)

    def importDataFromCsvFile(self, file_path: str):
        
        data = self.__csv_repo.find()

        insertedRows = self.importData(data)
        
            
    def createTable(self, table_name = None):
        name = self.__table_name
        if table_name != None: 
            name = table_name

        self.__dbRepo.createTable(name, [self.__trimColumnName(column) for column in self.__csv_repo.getColumns()])

    def importData(self, data: list):
        start = time.time()
        print(f"{Fore.CYAN}Inserting {Fore.GREEN}{self.__file_path} {Fore.CYAN}file...")
        insertedRows = 0
        for row in data:
            rowList = self.__prepareInsertData(row)
            self.__dbRepo.add(
                    {
                        "insert": rowList,
                        "into": self.__table_name 
                    }
                )
            insertedRows += 1
            if self.__should_log:
                self.__logInsertMessage(str(insertedRows), self.__file_path, self.__table_name)
                sys.stdout.write("\n")
            
        end = time.time()
        print(f"{Fore.CYAN}File {Fore.GREEN}{self.__file_path} {Fore.MAGENTA}({str(insertedRows)} rows) {Fore.CYAN}inserted in {Fore.MAGENTA}{int(end - start)}s")

        return insertedRows

    def getDivData(self, sub_list_no: int):
        data = self.__csv_repo.find()
        sub_list_len = len(data) // sub_list_no 
        if sub_list_len <= 0:
            raise ValueError("Rozmiar podlisty musi być większy niż 0.")

        sub_list = [data [i:i + sub_list_len] for i in range(0, len(data), sub_list_len)]
        return sub_list

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

    



