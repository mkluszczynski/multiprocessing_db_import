import matplotlib.pyplot as plt
from itertools import chain
    
class Chart:

    __chart_title: str 
    __processes_label: str = "Number of processes"
    __time_label: str = "Time taken to import in seconds [s]"

    __number_of_processes: list = [1, 2, 4, 8]
    __time_to_import: list[int]

    def __init__(self, chart_title: str, time_to_import: list[int]) -> None:
        self.__time_to_import = time_to_import 
        self.__chart_title = chart_title

    def create_summary_chart(chart_list: list):
        all_time_to_import = list(chain.from_iterable(list(map(lambda chart: chart.get_time_to_import(), chart_list))))
        summary = Chart.__process_time_summary([1, 2, 4, 8], all_time_to_import)
        return Chart("Multiprocessing performance", summary) 

    def show(self):
        plt.plot(self.__number_of_processes, self.__time_to_import, marker = 'o')
        plt.title(self.__chart_title)
        plt.xlabel(self.__processes_label)
        plt.ylabel(self.__time_label)
        plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
            
        for i, txt in enumerate(self.__time_to_import):
            plt.text(self.__number_of_processes[i], self.__time_to_import[i], str(txt), ha = 'right')
        plt.show()

    def get_time_to_import(self):
        return self.__time_to_import

    def __process_time_summary(process_count, time_to_import):
        sum_times = []
        for count in process_count:
            times = [time_to_import[i] for i in range(len(time_to_import)) if i % 4 == process_count.index(count)]
            sum_times.append(sum(times))
        return sum_times
