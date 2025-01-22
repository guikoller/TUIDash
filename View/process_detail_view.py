from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, Button, Footer, Static
from textual.screen import Screen

class ProcessDetail(Screen):
    BINDINGS = [("escape", "close", "Close")]
    CSS_PATH = "../Style/process_detail.tcss"

    def __init__(self, row_data) -> None:
        super().__init__()
        self.row_data = row_data

    def compose(self) -> ComposeResult:
        yield Footer()
        with Vertical(id="main-container"):
            yield Label(f"Process Details", id="header")
            yield Label(f"PID: {self.row_data['PID']}")
            yield Label(f"Name: {self.row_data['Name']}")
            yield Label(f"User: {self.row_data['User']}")
            yield Label(f"CPU (%): {self.row_data['CPU']}")
            yield Label(f"Memory (kB): {self.row_data['Memory']}")
            yield Label(f"Threads: {self.row_data['Threads']}")
            yield Label(f"Total Memory Pages: {self.row_data['Total Memory Pages']}")
            yield Label(f"Code Pages: {self.row_data['Code Pages']}")
            yield Label(f"Data Pages: {self.row_data['Data Pages']}")
            yield Label(f"Status: {self.row_data['Status']}")
            yield Static(expand=True)
            yield Button("Close", id="close")

    def action_close(self) -> None:
        self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.action_close()