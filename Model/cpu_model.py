import os
import time

class CPUModel:
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
        # returns the sum of all CPU times (total time) and the idle time (cpu_times[3])
        def parse_cpu_times():
            try:
                with open("/proc/stat", "r") as f:
                    first_line = f.readline()
                    cpu_times = list(map(int, first_line.split()[1:]))
                    return sum(cpu_times), cpu_times[3]  # Total and idle times
            except Exception as e:
                print(f"Error reading CPU usage: {e}")
                return 0, 0

        def calculate_cpu_usage():
            total_1, idle_1 = parse_cpu_times()
            time.sleep(0.1)
            total_2, idle_2 = parse_cpu_times()

            total_diff = total_2 - total_1
            idle_diff = idle_2 - idle_1
            usage = 100 * (1 - (idle_diff / total_diff)) if total_diff else 0
            return round(usage, 2)
        
        return calculate_cpu_usage()
    
    


