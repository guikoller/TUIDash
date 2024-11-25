# model/process_monitor.py

import psutil
import time

class ProcessMonitor:
    def fetch_process_list(self):
        """Fetch the list of current processes."""
        start_time = time.time()
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
                processes.append(proc.info)
            end_time = time.time()
            print(f"fetch_process_list took {end_time - start_time} seconds")
            return processes
        except Exception as e:
            print(f"Error fetching process list: {e}")
            return None