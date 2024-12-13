# class ProcessView:
#     def display_process_data(self, data):
#         print("\n--- Processes ---")
#         for process in data["processes"]:
#             print(f"Process ID: {process['PID']}, Name: {process['Name']}, User: {process['User']}, Memory: {process['Memory']} KB, Status: {process['Status']}, RunTime: {process['RunTime']} seconds")
#         print(data["total_processes"], "processes running")
        
        
from textual.app import  ComposeResult
from textual.widgets import DataTable
from textual.widget import Widget

COLUMNS = ["PID", "Name", "User", "Memory (kB)","CPU (%)", "Status"]


class ProcessView(Widget):
    # BINDINGS = [
    #     ("w", "sort_by_memory", "Sort By Memory"),
    #     ("e", "sort_by_time", "Sort By Time"),
    # ]
    current_sorts: set = set()
    
    def sort_reverse(self, sort_type: str):
        reverse = sort_type in self.current_sorts
        if reverse:
            self.current_sorts.remove(sort_type)
        else:
            self.current_sorts.add(sort_type)
        return reverse

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        for col in COLUMNS:
            table.add_column(col, key=col)
            
    def update(self, data):
        table = self.query_one(DataTable)
        table.clear()
        for process in data["processes"]:
            row = (process["PID"], process["Name"], process["User"], process["Memory"], process["CPU"], process["Status"])
            table.add_row(*row)
    

        
    
        
        