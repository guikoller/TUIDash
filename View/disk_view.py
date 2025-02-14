from textual.app import ComposeResult
from textual.widgets import Select, TextArea, Tree
from textual.widget import Widget
from Model.disk_model import DiskModel
from textual.reactive import reactive
from textual import on
import os

class DiskView(Widget):
    disk_info_text = reactive("")
    selected_partition = reactive(None)
    selected_directory = reactive(None)

    def __init__(self):
        super().__init__()
        self.disk_model = DiskModel()
        self.disk_info = self.disk_model.get_disk_info()
        self.partitions = self.disk_info.get('partitions', [])

    def compose(self) -> ComposeResult:
        yield Select(
            options=[
                (partition['Mountpoint'], partition['Mountpoint']) 
                for partition in self.partitions
            ],
            id="disk_select",
            name="Select Partition",
            classes="partition-select" 
        )
        yield TextArea(
            self.disk_info_text, 
            id="disk_info",
            read_only=True,
            disabled=True,
            name="Disk Information",
            classes="disk-info"
        )
        yield Tree(
            "Folders",
            id="folder_tree",
            name="Folder Structure",
            classes="folder-tree"  
        )

    @on(Select.Changed, "#disk_select")
    async def update_disk_info(self, event: Select.Changed) -> None:
        selected_disk = event.value
        self.selected_partition = selected_disk
        partition_info = next(
            (partition for partition in self.partitions if partition['Mountpoint'] == selected_disk), None
        )
        if partition_info:
            disk_info = (
                f"Device: {partition_info['Device']}\n"
                f"Mountpoint: {partition_info['Mountpoint']}\n"
                f"Total: {partition_info['Total']} GB\n"
                f"Used: {partition_info['Used']} GB\n"
                f"Free: {partition_info['Free']} GB\n"
                f"Usage: {partition_info['UsagePercent']} %"
            )
            await self.populate_tree(partition_info['Mountpoint'])
        else:
            disk_info = "No data available"
            self.clear_tree()
        self.query_one("#disk_info").text = disk_info

    async def populate_tree(self, mountpoint: str) -> None:
        tree = self.query_one("#folder_tree", Tree)
        tree.root.label = f"{mountpoint}"
        tree.root.data = mountpoint
        tree.root.remove_children()
        subdirs = await self.disk_model.get_subdirectories_async(mountpoint)
        tree.root.expandable = bool(subdirs)
        tree.root.refresh()

    def clear_tree(self) -> None:
        tree = self.query_one("#folder_tree", Tree)
        tree.root.remove_children()
        tree.root.label = "Folders"
        tree.root.data = ""
        tree.root.expandable = False
        tree.root.refresh()

    @on(Tree.NodeExpanded, "#folder_tree")
    async def load_children(self, event: Tree.NodeExpanded) -> None:
        node = event.node
        current_path = node.data

        if len(node.children) > 0:
            return

        subdirs_and_files = await self.disk_model.get_contents_async(current_path)
        for item_name, is_dir in subdirs_and_files:
            item_path = os.path.join(current_path, item_name)
            if is_dir:
                child_node = node.add(item_name, data=item_path)
                has_sub = await self.disk_model.get_subdirectories_async(item_path)
                child_node.expandable = bool(has_sub)
            else:
                node.add_leaf(item_name, data=item_path)

    @on(Tree.NodeSelected, "#folder_tree")
    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node = event.node
        selected_path = node.data

        if selected_path:
            self.selected_directory = selected_path

            if len(node.children) > 0:
                return

            contents = await self.disk_model.get_contents_async(selected_path)

            for item_name, is_dir in contents:
                item_path = os.path.join(selected_path, item_name)
                if is_dir:
                    child_node = node.add(item_name, data=item_path)
                    has_sub = await self.disk_model.get_subdirectories_async(item_path)
                    child_node.expandable = bool(has_sub)
                else:
                    node.add_leaf(item_name, data=item_path)