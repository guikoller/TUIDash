import os
import pwd
class ProcessModel:
    def get_process_list(self):
        all_processes = []

        for pid in os.listdir("/proc"):
            if pid.isdigit():
                with open(f"/proc/{pid}/stat", "r") as stat_file, open(f"/proc/{pid}/status", "r") as status_file:
                    # Read process name and memory usage
                    stat_data = stat_file.readline().split()
                    status_data = status_file.readlines()

                    uid = None
                    for line in status_data:
                        if line.startswith("Uid:"):
                            uid = int(line.split()[1])
                            break
                    user = pwd.getpwuid(uid).pw_name if uid is not None else "Unknown"

                    memory_usage = None
                    for line in status_data:
                        if line.startswith("VmRSS:"):
                            memory_usage = line.split(":")[1].strip()
                            break
                        
                    # Read process status and runtime
                    process_status = stat_data[2]
                    
                    start_time_ticks = int(stat_data[21])
                    clock_ticks_per_second = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
                    run_time_seconds = (start_time_ticks / clock_ticks_per_second)

                    all_processes.append({
                        "PID": pid,
                        "Name": stat_data[1].strip("()"),
                        "User": user,
                        "Memory": memory_usage,
                        "Status": process_status,
                        "RunTime": run_time_seconds
                    })


        return {
            "processes": all_processes,
            "total_processes": len(all_processes)
        }
