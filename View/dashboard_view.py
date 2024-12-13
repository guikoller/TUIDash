from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Placeholder
from textual.binding import Binding
from textual.containers import Grid
from textual.reactive import reactive


from View.system_view import SystemView
from View.process_view import ProcessView
from View.disk_view import DiskView


class DashboardView(App):
    CSS_PATH = "../Style/dashboard.tcss"
    
    data: reactive[dict] = {}
    
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        ("d", "toggle_dark", "Toggle dark mode")]    

    def __init__(self):
        super().__init__()
        self.system_view = SystemView()
        self.process_view = ProcessView()
        self.disk_view = DiskView()
        
        
    def update(self, data):
        print("-------------------------Updating view-------------------------")
        # print(data)
        self.system_view.update(data)
        self.process_view.update(data["Process List"])
        

    def compose(self) -> ComposeResult:
        yield Footer()
        with Grid():
            yield self.system_view
            yield self.disk_view
            yield self.process_view
