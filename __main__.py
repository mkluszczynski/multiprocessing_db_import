from os import listdir
from multiprocessing import Pool
from lib.Repository.DBRepository import DBRepository
from utils.Config import Config
from src.DBImporter import DBImporter
import time

dbRepo = DBRepository(
    Config.getDbHost(),
    Config.getDbPort(),
    Config.getDbUser(),
    Config.getDbPassword(),
    Config.getDbName()
)

dbImporter = DBImporter(dbRepo)

data_files = listdir("data")

def importig_data(data_files):
    for file in data_files:
        if file == ".gitkeep": continue
        print(file)
        dbImporter.importDataFromCsvFile("data/" + file)



if __name__ == "__main__":
    start = time.time()
    importig_data()
    end = time.time()
    print(f"Time taken without multiprocessing: {end-start}")
    
    time.sleep(1,5)

    start = time.time()
    pool = Pool()
    pool.map(importig_data, data_files)
    end = time.time()
    print(f"Time taken using multiprocessing: {end-start}")