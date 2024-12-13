import psutil
from operator import itemgetter
class DiskModel:
    def get_disk_info(self):
        disk_info = {"partitions": []}
        partitions = psutil.disk_partitions()
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info["partitions"].append({
                "Device": partition.device,
                "Mountpoint": partition.mountpoint,
                "FileSystemType": partition.fstype,
                "Total": usage.total,
                "Used": usage.used,
                "Free": usage.free,
                "UsagePercent": f"{usage.percent}%",
            })
        disk_info["partitions"].sort(key=itemgetter("Total"), reverse=True)

        return disk_info