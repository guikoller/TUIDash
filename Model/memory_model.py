class MemoryModel:
    def get_memory_info(self):
        memory_info = {}
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f.readlines():
                    if "MemTotal" in line:
                        memory_info["Total Memory"] = line.split(":")[1].strip()
                    elif "MemFree" in line:
                        memory_info["Free Memory"] = line.split(":")[1].strip()
                    elif "MemAvailable" in line:
                        memory_info["Available Memory"] = line.split(":")[1].strip()
        except FileNotFoundError:
            memory_info = {"Error": "Memory info only available on Linux systems."}
        return memory_info

    def get_memory_usage(self):
        try:
            with open("/proc/meminfo", "r") as f:
                meminfo = {}
                for line in f:
                    key, value = line.split(":")
                    meminfo[key.strip()] = int(value.split()[0])  #kB
                total_memory = meminfo["MemTotal"]
                available_memory = meminfo["MemAvailable"]
                used_memory = total_memory - available_memory
                usage_percentage = (used_memory / total_memory) * 100
                return round(usage_percentage, 2)
        except Exception as e:
            print(f"Error reading memory usage: {e}")
            return 0

    def get_swap_info(self):
        swap_info = {}
        try:
            with open("/proc/swaps", "r") as f:
                swap_data = f.readlines()
                if len(swap_data) > 1:
                    swap_info["Total Swap"] = swap_data[1].split()[2] + " kB"
                    swap_info["Used Swap"] = swap_data[1].split()[3] + " kB"
                else:
                    swap_info = {"Error": "No swap space available."}
        except FileNotFoundError:
            swap_info = {"Error": "Swap info only available on Linux systems."}
        return swap_info
