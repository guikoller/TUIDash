import psutil
from operator import itemgetter

def convert_to_gb(bytes):
    return f"{(bytes / (1024 ** 3)):.2f}"

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
                "Total": convert_to_gb(usage.total),
                "Used": convert_to_gb(usage.used),
                "Free": convert_to_gb(usage.free),
                "UsagePercent": f"{usage.percent}",
            })
        disk_info["partitions"].sort(key=itemgetter("Total"), reverse=True)

        return disk_info