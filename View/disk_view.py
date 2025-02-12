# disk_view.py

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
        # Assign class names to each widget for targeted styling
        yield Select(
            options=[
                (partition['Mountpoint'], partition['Mountpoint']) 
                for partition in self.partitions
            ],
            id="disk_select",
            name="Select Partition",
            classes="partition-select"  # Class for Select widget
        )
        yield TextArea(
            self.disk_info_text,  # Initial text as positional argument
            id="disk_info",
            read_only=True,
            disabled=True,
            name="Disk Information",
            classes="disk-info"  # Class for TextArea widget
        )
        yield Tree(
            "Folders",
            id="folder_tree",
            name="Folder Structure",
            classes="folder-tree"  # Class for Tree widget
        )

    @on(Select.Changed, "#disk_select")
    async def update_disk_info(self, event: Select.Changed) -> None:
        """
        Updates disk information and initializes the tree based on the selected partition.
        """
        selected_disk = event.value
        self.selected_partition = selected_disk
        partition_info = next(
            (partition for partition in self.partitions if partition['Mountpoint'] == selected_disk), None
        )
        if partition_info:
            # Update disk information text
            disk_info = (
                f"Device: {partition_info['Device']}\n"
                f"Mountpoint: {partition_info['Mountpoint']}\n"
                f"Total: {partition_info['Total']} GB\n"
                f"Used: {partition_info['Used']} GB\n"
                f"Free: {partition_info['Free']} GB\n"
                f"Usage: {partition_info['UsagePercent']} %"
            )
            # Populate the tree with the root directory of the selected partition
            await self.populate_tree(partition_info['Mountpoint'])
        else:
            disk_info = "No data available"
            self.clear_tree()
        # Update the TextArea with disk information
        self.query_one("#disk_info").text = disk_info

    async def populate_tree(self, mountpoint: str) -> None:
        """
        Initializes the Tree widget with the root directory of the selected partition.

        Args:
            mountpoint (str): The mount point of the selected partition.
        """
        tree = self.query_one("#folder_tree", Tree)
        # Set root node label and data
        tree.root.label = f"{mountpoint}"
        tree.root.data = mountpoint
        # Clear existing children
        tree.root.remove_children()
        # Fetch subdirectories asynchronously
        subdirs = await self.disk_model.get_subdirectories_async(mountpoint)
        # Mark root as expandable based on fetched subdirectories
        tree.root.expandable = bool(subdirs)
        # Refresh the tree to apply changes
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

        # Check if the node already has children to prevent reloading
        if len(node.children) > 0:
            return

        # Fetch subdirectories asynchronously
        subdirs = await self.disk_model.get_subdirectories_async(current_path)
        for subdir in subdirs:
            subdir_path = os.path.join(current_path, subdir)
            # Add the subdirectory as a child node
            child_node = node.add(subdir, data=subdir_path)
            # Determine if the subdirectory has further subdirectories asynchronously
            has_sub = await self.disk_model.get_subdirectories_async(subdir_path)
            child_node.expandable = bool(has_sub)

    @on(Tree.NodeSelected, "#folder_tree")
    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node = event.node
        selected_path = node.data

        if selected_path:
            self.selected_directory = selected_path

            # Check if the node already has children to prevent reloading
            if len(node.children) > 0:
                return

            # Fetch both folders and files asynchronously
            contents = await self.disk_model.get_contents_async(selected_path)

            for item_name, is_dir in contents:
                item_path = os.path.join(selected_path, item_name)
                # Add folders and files to the tree
                child_node = node.add(item_name, data=item_path)
                if is_dir:
                    # Mark as expandable if it is a folder
                    has_sub = await self.disk_model.get_subdirectories_async(item_path)
                    child_node.expandable = bool(has_sub)
                else:
                    # Files are not expandable
                    child_node.expandable = False
