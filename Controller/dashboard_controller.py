from threading import Thread
import time

from Model.memory_model import MemoryModel
from Model.cpu_model import CPUModel
from Model.process_model import ProcessModel
from Model.disk_model import DiskModel

from View.dashboard_view import DashboardView

class DashboardController:
    def __init__(self):
        self.cpu_model = CPUModel()
        self.memory_model = MemoryModel()
        self.process_model = ProcessModel()
        self.disk_model = DiskModel()
        
        self.view = DashboardView()

    def fetch_cpu_data(self, result):
        result["CPU Info"] = self.cpu_model.get_cpu_info()
        result["CPU Usage"] = self.cpu_model.get_cpu_usage()

    def fetch_memory_data(self, result):
        result["Memory Info"] = self.memory_model.get_memory_info()
        result["Memory Usage"] = self.memory_model.get_memory_usage()
        result["Swap Info"] = self.memory_model.get_swap_info()

    def fetch_process_data(self, result):
        result["Process List"] = self.process_model.get_process_list()
        
    def fetch_disk_data(self, result):
        result["Disk Info"] = self.disk_model.get_disk_info()

    def run_in_thread(self, target, args=()):
        thread = Thread(target=target, args=args)
        thread.start()
        return thread

    def update_data(self):
        while True:
            data = {}
            threads = [
                self.run_in_thread(self.fetch_cpu_data, (data,)),
                self.run_in_thread(self.fetch_memory_data, (data,)),
                self.run_in_thread(self.fetch_process_data, (data,)),
                self.run_in_thread(self.fetch_disk_data, (data,))
            ]

            for thread in threads:
                thread.join()
                
            self.view.update(data)
            print("Data updated")

            time.sleep(1)

    def run(self):
        thread = Thread(target=self.update_data)
        thread.start()
        self.view.run()
