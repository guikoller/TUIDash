import time
from threading import Thread
from Model.memory_model import MemoryModel
from Model.cpu_model import CPUModel
from Model.process_model import ProcessModel
from View.system_view import SystemView

class SystemController:
    def __init__(self):
        self.cpu_model = CPUModel()
        self.memory_model = MemoryModel()
        self.process_model = ProcessModel()
        self.view = SystemView()

    def fetch_cpu_data(self, result):
        result["CPU Info"] = self.cpu_model.get_cpu_info()
        result["CPU Usage"] = self.cpu_model.get_cpu_usage()

    def fetch_memory_data(self, result):
        result["Memory Info"] = self.memory_model.get_memory_info()
        result["Memory Usage"] = self.memory_model.get_memory_usage()
        result["Swap Info"] = self.memory_model.get_swap_info()

    def fetch_process_data(self, result):
        result["Process List"] = self.process_model.get_process_list()

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
                self.run_in_thread(self.fetch_process_data, (data,))
            ]

            for thread in threads:
                thread.join()

            self.view.display_system_data(data)
            time.sleep(5)

    def run(self):
        # Run the data update loop in the main thread
        self.update_data()