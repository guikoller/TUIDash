import asyncio
from concurrent.futures import ThreadPoolExecutor
import psutil
import os
from operator import itemgetter

def convert_to_gb(bytes_size):
    return f"{(bytes_size / (1024 ** 3)):.2f}"
class DiskModel:
    def __init__(self):
        self.executor = ThreadPoolExecutor()

    def get_disk_info(self):

        disk_info = {"partitions": []}
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
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
            except PermissionError:
                continue
            except Exception:
                continue
        disk_info["partitions"].sort(key=itemgetter("Total"), reverse=True)
        return disk_info

    def get_subdirectories(self, path):
        subdirs = []
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_dir(follow_symlinks=False):
                        subdirs.append(entry.name)
        except PermissionError:
            pass
        except Exception:
            pass
        return sorted(subdirs, key=str.lower)

    def get_contents(self, path):
        contents = []
        try:
            with os.scandir(path) as it:
                for entry in it:
                    contents.append( (entry.name, entry.is_dir(follow_symlinks=False)) )
        except PermissionError:
            contents.append( ("Permission Denied", False) )
        except Exception as e:
            contents.append( (f"Error: {str(e)}", False) )
        return sorted(contents, key=lambda x: (not x[1], x[0].lower()))

    async def get_subdirectories_async(self, path):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.get_subdirectories, path)

    async def get_contents_async(self, path):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.get_contents, path)