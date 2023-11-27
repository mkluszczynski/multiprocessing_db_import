from os import listdir
from multiprocessing import Pool 
from lib.Repository.DBRepository import DBRepository
from utils.Config import Config
from src.DBImporter import DBImporter
from src.charts import Charts
import time
import numpy as np
import matplotlib.pyplot as plt


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

    charts = Charts()
    eukaryotes_numOfProcesses = charts.eukaryotes_numOfProcesses
    eukaryotes_TimeToImport = charts.eukaryotes_TimeToImport    
    charts.labels(eukaryotes_numOfProcesses, eukaryotes_TimeToImport, "Number of processes", "Time taken to import in seconds [s]", "Eukaryotes 3775 KB")
    
    organelles_numOfProcesses = charts.organelles_numOfProcesses
    organelles_TimeToImport = charts.organelles_TimeToImport  
    charts.labels(organelles_numOfProcesses, organelles_TimeToImport, "Number of processes", "Time taken to import in seconds [s]", "Organelles 2544 KB")
    
    plasmids_numOfProcesses = charts.plasmids_numOfProcesses
    plasmids_TimeToImport = charts.plasmids_TimeToImport
    charts.labels(plasmids_numOfProcesses, plasmids_TimeToImport, "Number of processes", "Time taken to import in seconds [s]", "Plasmids 3985 KB")
    
    electric_vehicle_population_numOfProcesses = charts.electric_vehicle_population_numOfProcesses
    electric_vehicle_population_TimeToImport = charts.electric_vehicle_population_TimeToImport
    charts.labels(electric_vehicle_population_numOfProcesses, electric_vehicle_population_TimeToImport, "Number of processes", "Time taken to import in seconds [s]", "Electric Vehicle Population 35480 KB" )
    
    process_count = charts.process_count
    sum_times = charts.process_count
    charts.labels(process_count, sum_times,"Number of processes","Sum of time taken to import files on differenct processes [s]", "Multiprocessing performance")