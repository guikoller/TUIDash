# controller/dashboard_controller.py

import threading
import queue
import time
from Model.system_monitor import SystemMonitor
from Model.process_monitor import ProcessMonitor
from View.dashboard_view import DashboardView

class DashboardController:
    """Gerencia a interação entre Model e View com suporte a threads."""

    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.process_monitor = ProcessMonitor()
        self.dashboard_view = DashboardView()

        # Filas de comunicação
        self.collect_to_process_queue = queue.Queue()
        self.process_to_display_queue = queue.Queue()
        self.running = True

        # Start threads
        self.collect_thread = threading.Thread(target=self.collect_data, name="CollectThread")
        self.process_thread = threading.Thread(target=self.process_data, name="ProcessThread")
        self.collect_thread.start()
        self.process_thread.start()

        # Debugging statements to check if threads are running
        print(f"CollectThread is alive: {self.collect_thread.is_alive()}")
        print(f"ProcessThread is alive: {self.process_thread.is_alive()}")

    def collect_data(self):
        """Thread para coletar dados do sistema."""
        while self.running:
            start_time = time.time()  # Start timing
            data = {
                "cpu": self.system_monitor.fetch_cpu_usage(),
                "memory": self.system_monitor.fetch_memory_info(),
                "processes": self.process_monitor.fetch_process_list(),
            }
            end_time = time.time()  # End timing
            print(f"Collected data: {data}")  # Debugging statement
            print(f"Data collection took {end_time - start_time} seconds")  # Debugging statement
            self.collect_to_process_queue.put(data)
            time.sleep(1)  # Reduce the sleep interval to 1 second

    def process_data(self):
        """Thread para processar os dados coletados."""
        while self.running:
            if not self.collect_to_process_queue.empty():
                raw_data = self.collect_to_process_queue.get()
                print(f"Processing data: {raw_data}")  # Debugging statement
                if raw_data["memory"] is not None:
                    processed_data = {
                        "cpu": raw_data["cpu"],
                        "used_memory": raw_data["memory"]["used"] // (1024 ** 2),
                        "total_memory": raw_data["memory"]["total"] // (1024 ** 2),
                        "processes": raw_data["processes"],
                    }
                else:
                    processed_data = {
                        "cpu": raw_data["cpu"],
                        "used_memory": None,
                        "total_memory": None,
                        "processes": raw_data["processes"],
                    }
                self.process_to_display_queue.put(processed_data)
                self.update_view(processed_data)

    def update_view(self, data):
        """Update the view with the processed data."""
        self.dashboard_view.update_system_info(data)
        if data["processes"] is not None:
            self.dashboard_view.update_process_list(data["processes"])
        else:
            print("Process data not available")