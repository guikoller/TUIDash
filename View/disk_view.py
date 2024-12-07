class DiskView:
    def display_disk_data(self, disk_info):
        """
        Display disk and partition information.

        Args:
            disk_info (dict): Dictionary containing disk and partition information.
        """
        if "error" in disk_info:
            print(disk_info["error"])
            return

        print("\n=== Disk and Partition Information ===\n")
        for partition in disk_info["partitions"]:
            print(f"Device: {partition['Device']}")
            print(f"  Mountpoint: {partition['Mountpoint']}")
            print(f"  FileSystemType: {partition['FileSystemType']}")
            print(f"  Total: {partition['Total']}")
            print(f"  Used: {partition['Used']}")
            print(f"  Free: {partition['Free']}")
            print(f"  Usage: {partition['UsagePercent']}")
            print("-" * 40)
