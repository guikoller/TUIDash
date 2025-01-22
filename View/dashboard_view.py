from textual.app import App, ComposeResult
from textual.widgets import Footer
from textual.binding import Binding
from textual.containers import Grid
from textual.reactive import reactive

from View.system_view import SystemView
from View.process_view import ProcessView
from View.disk_view import DiskView
from View.process_detail_view import ProcessDetail

class DashboardView(App):
    CSS_PATH = "../Style/dashboard.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="d", action="toggle_dark", description="Toggle dark mode"),
        Binding(key="f", action="freeze_update", description="Freeze update")
    ]

    def __init__(self):
        super().__init__()
        self.freeze = True
        self.system_view = SystemView()
        self.process_view = ProcessView()
        self.disk_view = DiskView()
        self.process_detail = None  # Initialize as None

    def update(self, data):
        if self.freeze:
            self.system_view.update(data)
            self.process_view.update(data["Process List"])

    def compose(self) -> ComposeResult:
        yield Footer()
        with Grid():
            yield self.system_view
            yield self.disk_view
            yield self.process_view

    def action_freeze_update(self):
        self.freeze = not self.freeze

    def on_process_view_row_selected(self, message: ProcessView.RowSelected) -> None:
        row_data = message.row_data
        # Create a new ProcessDetail screen with the row_data
        self.process_detail = ProcessDetail(row_data)
        self.push_screen(self.process_detail)