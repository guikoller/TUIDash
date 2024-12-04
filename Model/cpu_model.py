import os
import time

class CPUModel:
    def get_cpu_info():
        cpu_info = {"CPU Cores": os.cpu_count()}
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f.readlines():
                    if "model name" in line:
                        cpu_info["CPU Model"] = line.split(":")[1].strip()
                        break
        except FileNotFoundError:
            cpu_info["CPU Model"] = "Unknown"
        return cpu_info

    def get_cpu_usage():
        def parse_cpu_times():
            with open("/proc/stat", "r") as f:
                line = f.readline()
                times = list(map(int, line.split()[1:]))
            return sum(times), times[3]

        total1, idle1 = parse_cpu_times()
        time.sleep(0.1)
        total2, idle2 = parse_cpu_times()
        total_diff = total2 - total1
        idle_diff = idle2 - idle1
        return round(100 * (1 - idle_diff / total_diff), 2) if total_diff else 0
