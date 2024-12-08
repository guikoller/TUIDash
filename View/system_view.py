from textual.widget import Widget
from textual.widgets import Static, ProgressBar, Markdown, TextArea
from textual.reactive import Reactive
from textual.app import ComposeResult

class SystemView(Widget):
    CSS_PATH = "../Style/system.tcss"
    
    cpu_info = Reactive("")
    cpu_usage = Reactive(0)
    memory_info = Reactive("")
    memory_usage = Reactive(0)

    def compose(self) -> ComposeResult:
        yield Static("CPU Info:")
        yield TextArea(id="cpu_info", read_only = True, disabled=True)  
        yield Static("CPU Usage:")
        yield ProgressBar(id="cpu_usage", total=100, show_eta=False)
        yield Static("Memory Info:")
        yield TextArea(id="memory_info", read_only = True, disabled=True)
        yield Static("Memory Usage:")
        yield ProgressBar(id="memory_usage", total=100, show_eta=False)

    def update_memory_info(self, memory_info):
        total_memory = memory_info["Total Memory"]
        free_memory = memory_info["Free Memory"]
        available_memory = memory_info["Available Memory"]
        memory_info_text = f"Total: {total_memory}\nFree: {free_memory}\nAvailable: {available_memory}"
        self.query_one("#memory_info").text = memory_info_text
    
    
    def update_cpu_info(self, cpu_info):
        cpu_cores = cpu_info["CPU Cores"]
        cpu_model = cpu_info["CPU Model"]
        cpu_info_text = f"Model: {cpu_model}\nCores: {cpu_cores}"
        self.query_one("#cpu_info").text=cpu_info_text

        
    def update(self, data):
        self.query_one("#cpu_usage").update(progress= data["CPU Usage"])
        self.update_memory_info(data["Memory Info"])
        self.update_cpu_info(data["CPU Info"])
        self.query_one("#memory_usage").update(progress= data["Memory Usage"])