import os

from View.system_view import SystemView
from View.process_view import ProcessView
from View.disk_view import DiskView

class DashboardView:
    def __init__(self):
        self.system_view = SystemView()
        self.process_view = ProcessView()
        self.disk_view = DiskView()
        
    def clear_console(self):
         os.system('clear')

    def display_dashboard(self, data):
        self.clear_console()
        print("\n====== System Dashboard ======\n")
        self.system_view.display_system_data(data)
        self.process_view.display_process_data(data["Process List"])
        self.disk_view.display_disk_data(data["Disk Info"])
        print("================================\n")
        

