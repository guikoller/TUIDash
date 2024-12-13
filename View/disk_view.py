from textual.app import ComposeResult
from textual.widgets import Select, TextArea
from textual.widget import Widget
from Model.disk_model import DiskModel
from textual.reactive import reactive
from textual import on

class DiskView(Widget):
    disk_info_text = reactive("")

    def __init__(self, ):
        super().__init__()
        self.disk_model = DiskModel()
        self.disk_info = self.disk_model.get_disk_info()
        self.partitions = self.disk_info.get('partitions', [])

    def compose(self) -> ComposeResult:
        options = [(partition['Device'], partition['Device']) for partition in self.partitions]
        yield Select(options=options, id="disk_select")
        yield TextArea(self.disk_info_text, id="disk_info", read_only = True, disabled=True)

    @on(Select.Changed)
    def update_disk_info(self, event: Select.Changed) -> None:
        selected_disk = event.value
        partition_info = next((partition for partition in self.partitions if partition['Device'] == selected_disk), None)
        if partition_info:
            disk_info = (
                f"Device: {partition_info['Device']}\n"
                f"Mountpoint: {partition_info['Mountpoint']}\n"
                f"Total: {partition_info['Total']}\n"
                f"Used: {partition_info['Used']}\n"
                f"Free: {partition_info['Free']}\n"
                f"Usage: {partition_info['UsagePercent']}"
            )
        else:
            disk_info = "No data available"
        self.query_one("#disk_info").text=disk_info
