from os import listdir
from multiprocessing import Pool 
from itertools import chain
from lib.Repository.DBRepository import DBRepository
from utils.Config import Config
from src.DBImporter import DBImporter
from src.Chart import Chart
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


def show_chart(chart: Chart):
        chart.show()

def process_time_summary(process_count, time_to_import):
        sum_times = []
        for count in process_count:
            times = [time_to_import[i] for i in range(len(time_to_import)) if i % 4 == process_count.index(count)]
            sum_times.append(sum(times))
        return sum_times


     
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

    eukaryotes_chart = Chart("Eukaryotes 3775 K" ,[34, 20, 12, 7])
    organelles_chart = Chart("Organelles 2544 KB", [49, 28, 17, 10])
    plasmids_chart = Chart("Plasmids 3985 KB", [62, 36, 22, 13])
    electric_chart = Chart("Electric Vehicle Population 35480 KB", [1813, 888, 519, 284])

    chart_list = [eukaryotes_chart, organelles_chart, plasmids_chart, electric_chart]

    summary_chart = Chart.create_summary_chart(chart_list)

    chart_list.append(summary_chart)

    pool = Pool(len(chart_list))
    pool.map(show_chart, chart_list)