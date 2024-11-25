# view/dashboard_view.py

from View.system_info_view import SystemInfoView
from View.process_list_view import ProcessListView

class DashboardView:
    def __init__(self):
        self.system_info_view = SystemInfoView()
        self.process_list_view = ProcessListView()

    def update_system_info(self, data):
        """Update the system info view with the new data."""
        system_info = {
            "cpu_usage": data["cpu"],
            "total_memory": data["total_memory"],
            "used_memory": data["used_memory"],
            "free_memory": data["total_memory"] - data["used_memory"] if data["total_memory"] and data["used_memory"] else None
        }
        self.system_info_view.update_info(system_info)

    def update_process_list(self, processes):
        """Update the process list view with the new processes."""
        self.process_list_view.update_processes(processes)