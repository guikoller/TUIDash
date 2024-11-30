# Model: Responsible for gathering system data

import os
import time
import threading
import pwd

class SystemModel:
    def get_cpu_info(self):
        cpu_count_logical = os.cpu_count()
        cpu_info = {"CPU Cores": cpu_count_logical}

        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f.readlines():
                    if "model name" in line:
                        cpu_info["CPU Model"] = line.split(":")[1].strip()
                        break
            if "CPU Model" not in cpu_info:
                cpu_info["CPU Model"] = "Unknown CPU Model"
        except FileNotFoundError:
            cpu_info["CPU Model"] = "Not available (Linux only)"
        
        return cpu_info

    def get_cpu_usage(self):
        def parse_cpu_times():
            try:
                with open("/proc/stat", "r") as f:
                    first_line = f.readline()
                    cpu_times = list(map(int, first_line.split()[1:]))
                    return sum(cpu_times), cpu_times[3]  # Total and idle times
            except Exception as e:
                print(f"Error reading CPU usage: {e}")
                return 0, 0

        total_1, idle_1 = parse_cpu_times()
        time.sleep(0.1)
        total_2, idle_2 = parse_cpu_times()

        total_diff = total_2 - total_1
        idle_diff = idle_2 - idle_1
        usage = 100 * (1 - (idle_diff / total_diff)) if total_diff else 0
        return round(usage, 2)

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
                    meminfo[key.strip()] = int(value.split()[0])  # Convert to kB
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

    def get_process_list(self, limit=20):
        processes = []
        try:
            for pid in os.listdir("/proc"):
                if pid.isdigit():
                    with open(f"/proc/{pid}/stat", "r") as stat_file, open(f"/proc/{pid}/status", "r") as status_file:
                        # Read process name and memory usage
                        stat_data = stat_file.readline().split()
                        status_data = status_file.readlines()

                        # Get user ID and convert it to username
                        uid = None
                        for line in status_data:
                            if line.startswith("Uid:"):
                                uid = int(line.split()[1])
                                break
                        user = pwd.getpwuid(uid).pw_name if uid else "Unknown"

                        # Get memory usage
                        memory_usage = None
                        for line in status_data:
                            if line.startswith("VmRSS:"):
                                memory_usage = line.split(":")[1].strip()
                                break

                        processes.append({
                            "PID": pid,
                            "Name": stat_data[1].strip("()"),
                            "User": user,
                            "Memory": memory_usage or "N/A"
                        })

                        if len(processes) >= limit:
                            break
        except Exception as e:
            print(f"Error reading processes: {e}")
        return processes
