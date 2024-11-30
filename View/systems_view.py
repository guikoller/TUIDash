# View: Responsible for displaying the system data

import os

class SystemView:
    def display_cpu_info(self, cpu_info, usage):
        print("CPU Info:")
        for key, value in cpu_info.items():
            print(f"{key}: {value}")
        print(f"CPU Usage: {usage}%\n")

    def display_memory_info(self, memory_info, usage):
        print("Memory Info:")
        for key, value in memory_info.items():
            print(f"{key}: {value}")
        print(f"Memory Usage: {usage}%\n")

    def display_swap_info(self, swap_info):
        print("Swap Info:")
        for key, value in swap_info.items():
            print(f"{key}: {value}")
        print()

    def display_process_list(self, processes):
        print("Top Processes:")
        for process in processes:
            print(f"PID: {process['PID']}, Name: {process['Name']}, User: {process['User']}, Memory: {process['Memory']}")
        print()

    def clear_console(self):
        os.system('clear' if os.name == 'posix' else 'cls')