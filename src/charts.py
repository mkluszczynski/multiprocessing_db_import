import matplotlib.pyplot as plt
import numpy as np

class Charts:
    def __init__(self) -> None:
        eukaryotes_numOfProcesses = np.array([1, 2, 4, 8])
        eukaryotes_TimeToImport = np.array([34, 20, 12, 7])
        
        plasmids_numOfProcesses = np.array([1, 2, 4, 8])
        plasmids_TimeToImport =  np.array([62, 36, 22, 13])
            
        electric_vehicle_population_numOfProcesses = np.array([1, 2, 4, 8])
        electric_vehicle_population_TimeToImport = np.array([1813, 888, 519, 284])
            
        organelles_numOfProcesses = np.array([1, 2, 4, 8])
        organelles_TimeToImport = np.array([49, 28, 17, 10])
            
        process_count = [1, 2, 4, 8]
        time_to_import = [34, 20, 12, 7, 49, 28, 17, 10, 62, 36, 22, 13, 1813, 888, 519, 284]

        
    
    def labels(x_data, y_data,x_label, y_label, title):
        plt.plot(x_data, y_data, marker = 'o')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
            
        for i, txt in enumerate(y_data):
            plt.text(x_data[i], y_data[i], str(txt), ha = 'right')
        plt.show()
    
    def process_time_summary(self, process_count, time_to_import):
        sum_times = []
        for count in process_count:
            times = [time_to_import[i] for i in range(len(time_to_import)) if i % 4 == process_count.index(count)]
            sum_times.append(sum(times))
        return sum_times

    