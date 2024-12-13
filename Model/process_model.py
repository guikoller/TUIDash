import os
import pwd

class ProcessModel:
    def get_process_list(self):
        all_processes = []

        for pid in os.listdir("/proc"):
            if pid.isdigit():
                with open(f"/proc/{pid}/stat", "r") as stat_file, open(f"/proc/{pid}/status", "r") as status_file, open(f"/proc/{pid}/statm", "r") as statm_file:
                    # Read process name and memory usage
                    stat_data = stat_file.readline().split()
                    status_data = status_file.readlines()
                    statm_data = statm_file.readline().split()

                    uid = None
                    for line in status_data:
                        if line.startswith("Uid:"):
                            uid = int(line.split()[1])
                            break
                    user = pwd.getpwuid(uid).pw_name if uid is not None else "Unknown"

                    memory_usage = None
                    for line in status_data:
                        if line.startswith("VmRSS:"):
                            memory_usage = int(line.split(":")[1].strip().replace(" kB", ""))
                            break
                        else:
                            memory_usage = 0

                    # Read process status and runtime
                    process_status = stat_data[2]

                    start_time_ticks = int(stat_data[21])
                    clock_ticks_per_second = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

                    # Calculate CPU usage
                    total_time = int(stat_data[13]) + int(stat_data[14]) + int(stat_data[15]) + int(stat_data[16])
                    uptime = float(open("/proc/uptime", "r").readline().split()[0])
                    cpu_usage = 100 * ((total_time / clock_ticks_per_second) / uptime)

                    # Read memory pages information
                    total_memory_pages = int(statm_data[0])
                    code_pages = int(statm_data[1])
                    data_pages = int(statm_data[5])
                    stack_pages = int(statm_data[6])
                    
                    # Count the number of threads
                    task_dir = f"/proc/{pid}/task"
                    num_threads = len(os.listdir(task_dir))

                    all_processes.append({
                        "PID": pid,
                        "Name": stat_data[1].strip("()"),
                        "User": user,
                        "Memory": memory_usage,
                        "Status": process_status,
                        "CPU": cpu_usage,
                        "Total Memory Pages": total_memory_pages,
                        "Code Pages": code_pages,
                        "Data Pages": data_pages,
                        "Stack Pages": stack_pages,
                        "Threads": num_threads
                    })
            
                    all_processes.sort(key=lambda x: x["CPU"], reverse=True)
                    
        return {
            "processes": all_processes,
            "total_processes": len(all_processes)
        }
