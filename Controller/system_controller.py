# Controller: Manages the data flow between Model and View

import time
from Model.systems_model import SystemModel
from View.systems_view import SystemView

class SystemController:
    def __init__(self):
        self.model = SystemModel()
        self.view = SystemView()

    def update_system_data(self):
        cpu_info = self.model.get_cpu_info()
        cpu_usage = self.model.get_cpu_usage()
        memory_info = self.model.get_memory_info()
        memory_usage = self.model.get_memory_usage()
        swap_info = self.model.get_swap_info()
        processes = self.model.get_process_list()

        self.view.clear_console()
        self.view.display_cpu_info(cpu_info, cpu_usage)
        self.view.display_memory_info(memory_info, memory_usage)
        self.view.display_swap_info(swap_info)
        self.view.display_process_list(processes)

    def run(self):
        while True:
            self.update_system_data()
            time.sleep(1)