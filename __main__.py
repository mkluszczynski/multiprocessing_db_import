from os import listdir

from lib.Repository.DBRepository import DBRepository
from utils.Config import Config
from src.DBImporter import DBImporter

dbRepo = DBRepository(
    Config.getDbHost(),
    Config.getDbPort(),
    Config.getDbUser(),
    Config.getDbPassword(),
    Config.getDbName()
)

dbImporter = DBImporter(dbRepo)

data_files = listdir("data")

for file in data_files:
    if file == ".gitkeep": continue
    print(file)
    dbImporter.importDataFromCsvFile("data/" + file)