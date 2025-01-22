from textual.app import ComposeResult
from textual.widgets import DataTable
from textual.widget import Widget
from textual.events import Click
from textual.message import Message

COLUMNS = [
    "PID",
    "Name",
    "User",
    "CPU (%)",
    "Memory (kB)",
    "Threads",
    "Total Memory Pages",
    "Code Pages",
    "Data Pages",
    "Status"
]

class ProcessView(Widget):
    current_sorts: set = set()
    actutal_rows = None

    class RowSelected(Message):
        def __init__(self, row_data) -> None:
            super().__init__()
            self.row_data = row_data

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

        table.cursor_type = "row"
        table.add_class("clickable")

    def update(self, data):
        table = self.query_one(DataTable)
        table.clear()
        self.actutal_rows = []
        for process in data["processes"]:
            row = (
                process["PID"],
                process["Name"],
                process["User"],
                process["CPU"],
                process["Memory"],
                process["Threads"],
                process["Total Memory Pages"],
                process["Code Pages"],
                process["Data Pages"],
                process["Status"]
            )
            table.add_row(*row)
            self.actutal_rows.append(process)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        row_index = event.cursor_row
        row_data = self.actutal_rows[row_index]
        print(row_data)
        self.post_message(self.RowSelected(row_data))