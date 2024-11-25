# view/system_info_view.py

class SystemInfoView:
    def update_info(self, info):
        """Update the system info view with the new data."""
        system_info = (
            f"CPU Usage: {info['cpu_usage']}%\n"
            f"Total Memory: {info['total_memory']} MB\n"
            f"Used Memory: {info['used_memory']} MB\n"
            f"Free Memory: {info['free_memory']} MB\n"
        )
        print(system_info)