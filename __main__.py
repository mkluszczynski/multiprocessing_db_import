from os import listdir
from time import sleep
from multiprocessing import Pool

from lib.Repository.DBRepository import DBRepository
from utils.Config import Config
from src.DBImporter import DBImporter

data_files_names = listdir("data")
data_files = list(map(lambda file_name: f"data/{file_name}", data_files_names))

def import_csv (file_path: str):
    if file_path == ".gitkeep": return 

    dbRepo = DBRepository(
        Config.getDbHost(),
        Config.getDbPort(),
        Config.getDbUser(),
        Config.getDbPassword(),
        Config.getDbName()
    )
    dbImporter = DBImporter(dbRepo)
    dbImporter.importDataFromCsvFile(file_path, False)


pool = Pool(len(data_files))
pool.map(import_csv, data_files)