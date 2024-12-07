import psutil

class DiskModel:
    def get_disk_info(self):
        disk_info = {"partitions": []}

        try:
            partitions = psutil.disk_partitions()
            for partition in partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info["partitions"].append({
                    "Device": partition.device,
                    "Mountpoint": partition.mountpoint,
                    "FileSystemType": partition.fstype,
                    "Total": f"{usage.total // (1024 ** 3)} GB",
                    "Used": f"{usage.used // (1024 ** 3)} GB",
                    "Free": f"{usage.free // (1024 ** 3)} GB",
                    "UsagePercent": f"{usage.percent}%",
                })
        except Exception as e:
            disk_info["error"] = f"Error retrieving disk information: {e}"

        return disk_info
