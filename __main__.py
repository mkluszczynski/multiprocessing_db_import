from sys import argv
from os import listdir
from os.path import getsize
from multiprocessing import Pool 
from lib.Repository.DBRepository import DBRepository
from lib.Repository.CSVRepository import CSVRepository
from utils.Config import Config
from src.DBImporter import DBImporter
import time

data_files_names = listdir("data")
data_files = list(map(lambda file_name: f"data/{file_name}", data_files_names))

def import_file(file, shouldLog = False):
    if file == "data/.gitkeep": return
    dbRepo = DBRepository(
        Config.getDbHost(),
        Config.getDbPort(),
        Config.getDbUser(),
        Config.getDbPassword(),
        Config.getDbName()
    )

    dbImporter = DBImporter(dbRepo, file, file)
    dbImporter.importDataFromCsvFile(file)

def import_file_multiprocess(data: list):
    if file == "data/.gitkeep": return
    dbRepo = DBRepository(
        Config.getDbHost(),
        Config.getDbPort(),
        Config.getDbUser(),
        Config.getDbPassword(),
        Config.getDbName()
    )

    dbImporter = DBImporter(dbRepo, argv[1], argv[1])
    dbImporter.importData(data)

def divList(data_list: list, sub_list_no: int):
        sub_list_len = len(data_list) // sub_list_no 
        if sub_list_len <= 0:
            raise ValueError("Rozmiar podlisty musi być większy niż 0.")

        sub_list = [data_list[i:i + sub_list_len] for i in range(0, len(data_list), sub_list_len)]
        return sub_list 

if __name__ == "__main__":
    # start = time.time()
    # for file in data_files:
    #     import_file(file, True) 
    # end = time.time()
    # print(f"Time taken without multiprocessing: {int(end - start)}")
    

    # start = time.time()
    # pool = Pool(len(data_files)) 
    # pool.map(import_file, data_files)
    # end = time.time()
    # print(f"Time taken using multiprocessing: {int(end - start)}")
    if len(argv) == 1:
        print("File path argument required!")
        exit(1)
    
    process_number = 1
    if len(argv) > 2:
        process_number = int(argv[2])

    file_path = argv[1]

    print(f"File path: {file_path} File size: {int(getsize(file_path)//1024)} KB Number of procceses: {process_number}") 

    dbRepo = DBRepository(
        Config.getDbHost(),
        Config.getDbPort(),
        Config.getDbUser(),
        Config.getDbPassword(),
        Config.getDbName()
    )

    dbImporter = DBImporter(dbRepo, argv[1], argv[1])
    dbImporter.createTable()

    start = time.time()
    file = open(file_path)
    csvRepo = CSVRepository(file)
    base_data = csvRepo.find()
    data_list = divList(base_data, process_number)

    pool = Pool(len(data_list))    
    pool.map(import_file_multiprocess, data_list)

    end = time.time()

    print(f"Time taken using multiprocessing: {int(end - start)}")
