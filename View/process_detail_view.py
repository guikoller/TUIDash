from textual.app import ComposeResult
from textual.containers import Grid, ScrollableContainer
from textual.widgets import Label, Button, DataTable
from textual.screen import Screen

class ProcessDetail(Screen):
    BINDINGS = [("escape", "close", "Close")]
    CSS_PATH = "../Style/process_detail.tcss"

    def __init__(self, row_data) -> None:
        super().__init__()
        self.row_data = row_data

    def compose(self) -> ComposeResult:
        # Main Grid
        with Grid(id="main-grid"):
            # Header
            yield Label("Process Details", id="header")

            # Content Grid
            with Grid(id="content-grid"):
                # Basic Information Section
                with Grid(id="basic-info"):
                    yield Label(f"PID: {self.row_data['PID']}")
                    yield Label(f"Name: {self.row_data['Name']}")
                    yield Label(f"User: {self.row_data['User']}")
                    yield Label(f"Status: {self.row_data['Status']}")
                    yield Label(f"CPU (%): {self.row_data['CPU']:.2f}")
                    yield Label(f"Memory (kB): {self.row_data['Memory']}")
                    yield Label(f"Threads: {self.row_data['Threads']}")

                # Resource Counts Section
                with Grid(id="resource-counts"):
                    yield Label(f"Open Files: {self.row_data.get('Open Files Count', 0)}")
                    yield Label(f"Open Sockets: {self.row_data.get('Open Sockets Count', 0)}")
                    yield Label(f"Open Pipes: {self.row_data.get('Open Pipes Count', 0)}")
                    yield Label(f"Semaphores: {self.row_data.get('Semaphores Count', 0)}")

            # Scrollable Resource Details
            with ScrollableContainer(id="resource-details"):
                yield Label("Resource Details", id="section-header")

                # Open Files Table
                open_files_list = self.row_data.get('Open Files', [])
                if open_files_list:
                    yield Label("Open Files:", classes="subsection-header")
                    open_files_table = DataTable(id="open-files-table")
                    open_files_table.add_column("File Descriptor")
                    open_files_table.add_column("File Path")
                    for fd_info in open_files_list:
                        fd_num = fd_info['fd']
                        fd_path = fd_info['path']
                        open_files_table.add_row(str(fd_num), fd_path)
                    yield open_files_table

                # Open Sockets Table
                open_sockets_list = self.row_data.get('Open Sockets', [])
                if open_sockets_list:
                    yield Label("Open Sockets:", classes="subsection-header")
                    open_sockets_table = DataTable(id="open-sockets-table")
                    open_sockets_table.add_column("Socket Descriptor")
                    open_sockets_table.add_column("Socket Info")
                    for socket_info in open_sockets_list:
                        fd_num = socket_info['fd']
                        description = socket_info['description']
                        open_sockets_table.add_row(str(fd_num), description)
                    yield open_sockets_table

                # Open Pipes Table
                open_pipes_list = self.row_data.get('Open Pipes', [])
                if open_pipes_list:
                    yield Label("Open Pipes:", classes="subsection-header")
                    open_pipes_table = DataTable(id="open-pipes-table")
                    open_pipes_table.add_column("Pipe Descriptor")
                    open_pipes_table.add_column("Pipe Info")
                    for pipe_info in open_pipes_list:
                        fd_num = pipe_info['fd']
                        description = pipe_info['description']
                        open_pipes_table.add_row(str(fd_num), description)
                    yield open_pipes_table

                # Semaphores Table
                semaphores_list = self.row_data.get('Semaphores', [])
                if semaphores_list:
                    yield Label("Semaphores:", classes="subsection-header")
                    semaphores_table = DataTable(id="semaphores-table")
                    semaphores_table.add_column("Semaphore ID")
                    semaphores_table.add_column("Key")
                    semaphores_table.add_column("Owner UID")
                    for sem_info in semaphores_list:
                        sem_id = sem_info['id']
                        key = sem_info['key']
                        uid = sem_info['uid']
                        semaphores_table.add_row(str(sem_id), str(key), str(uid))
                    yield semaphores_table

            # Close Button
            yield Button("Close", id="close")

    def action_close(self) -> None:
        self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.action_close()