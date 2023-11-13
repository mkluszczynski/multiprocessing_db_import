from os import listdir
from multiprocessing import Pool 
from lib.Repository.DBRepository import DBRepository
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

    dbImporter = DBImporter(dbRepo)
    dbImporter.importDataFromCsvFile(file, shouldLog)


if __name__ == "__main__":
    start = time.time()
    for file in data_files:
        import_file(file, True) 
    end = time.time()
    print(f"Time taken without multiprocessing: {int(end - start)}")
    

    start = time.time()
    pool = Pool(len(data_files)) 
    pool.map(import_file, data_files)
    end = time.time()
    print(f"Time taken using multiprocessing: {int(end - start)}")
