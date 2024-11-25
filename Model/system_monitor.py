# model/system_monitor.py

import psutil
import time

class SystemMonitor:
    def __init__(self):
        # Initial call to get immediate CPU usage
        self.initial_cpu_usage = psutil.cpu_percent(interval=None)

    def fetch_cpu_usage(self):
        """Fetch the current CPU usage percentage."""
        start_time = time.time()
        try:
            # Use interval=None for the first call to avoid delay
            cpu_usage = psutil.cpu_percent(interval=None if self.initial_cpu_usage is None else 1)
            self.initial_cpu_usage = None  # Reset after the first call
            end_time = time.time()
            print(f"fetch_cpu_usage took {end_time - start_time} seconds")
            return cpu_usage
        except Exception as e:
            print(f"Error fetching CPU usage: {e}")
            return None

    def fetch_memory_info(self):
        """Fetch the current memory usage information."""
        start_time = time.time()
        try:
            memory_info = psutil.virtual_memory()
            end_time = time.time()
            print(f"fetch_memory_info took {end_time - start_time} seconds")
            return {
                "total": memory_info.total,
                "used": memory_info.used,
                "free": memory_info.free
            }
        except Exception as e:
            print(f"Error fetching memory info: {e}")
            return None