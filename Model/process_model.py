import os
import pwd

class ProcessModel:
    def get_process_list(self):
        all_processes = []

        for pid in os.listdir("/proc"):
            if pid.isdigit():
                try:
                    with open(f"/proc/{pid}/stat", "r") as stat_file, \
                         open(f"/proc/{pid}/status", "r") as status_file, \
                         open(f"/proc/{pid}/statm", "r") as statm_file:

                        stat_data = stat_file.readline().split()
                        status_data = status_file.readlines()
                        statm_data = statm_file.readline().split()

                        # UID and Username
                        uid = None
                        for line in status_data:
                            if line.startswith("Uid:"):
                                uid = int(line.split()[1])
                                break
                        user = pwd.getpwuid(uid).pw_name if uid is not None else "Unknown"

                        # Memory Usage (VmRSS)
                        memory_usage = None
                        for line in status_data:
                            if line.startswith("VmRSS:"):
                                memory_usage = int(line.split()[1])
                                break
                        if memory_usage is None:
                            memory_usage = 0

                        # Process Status
                        process_status = stat_data[2]

                        # CPU Usage
                        clock_ticks_per_second = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
                        total_time = int(stat_data[13]) + int(stat_data[14])
                        uptime = float(open("/proc/uptime", "r").readline().split()[0])
                        cpu_usage = 100 * ((total_time / clock_ticks_per_second) / uptime)

                        # Memory Pages
                        total_memory_pages = int(statm_data[0])
                        code_pages = int(statm_data[1])
                        data_pages = int(statm_data[5])
                        stack_pages = int(statm_data[6])

                        # Number of Threads
                        task_dir = f"/proc/{pid}/task"
                        num_threads = len(os.listdir(task_dir))

                        # Open Files, Sockets, Pipes
                        fd_dir = f"/proc/{pid}/fd"
                        open_files_list = []
                        open_sockets_list = []
                        open_pipes_list = []
                        try:
                            fds = os.listdir(fd_dir)
                            for fd in fds:
                                fd_path = os.path.join(fd_dir, fd)
                                try:
                                    target = os.readlink(fd_path)
                                    fd_info = {'fd': fd, 'path': target}
                                    if target.startswith('socket:'):
                                        open_sockets_list.append({'fd': fd, 'description': target})
                                    elif target.startswith('pipe:'):
                                        open_pipes_list.append({'fd': fd, 'description': target})
                                    else:
                                        open_files_list.append(fd_info)
                                except FileNotFoundError:
                                    continue
                                except PermissionError:
                                    continue
                        except FileNotFoundError:
                            pass
                        except PermissionError:
                            pass

                        # Counts
                        open_files_count = len(open_files_list)
                        open_sockets_count = len(open_sockets_list)
                        open_pipes_count = len(open_pipes_list)
                        semaphores_list = []
                        semaphores_count = 0

                        
                        semaphores_path = f"/proc/{pid}/sysvipc/sem"
                        if os.path.exists(semaphores_path):
                            with open(semaphores_path, "r") as sem_file:
                                for line in sem_file:
                                    if line.strip():
                                        semaphores_list.append(line.strip())
                                        semaphores_count += 1

                        # Build process information dictionary
                        process_info = {
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
                            "Threads": num_threads,
                            "Open Files Count": open_files_count,
                            "Open Sockets Count": open_sockets_count,
                            "Open Pipes Count": open_pipes_count,
                            "Open Files": open_files_list,
                            "Open Sockets": open_sockets_list,
                            "Open Pipes": open_pipes_list,
                            "Semaphores Count": semaphores_count,
                            "Semaphores": semaphores_list,
                        }

                        all_processes.append(process_info)

                except FileNotFoundError:
                    continue
                except PermissionError:
                    continue
                except Exception as e:
                    continue

        all_processes.sort(key=lambda x: x["CPU"], reverse=True)

        return {
            "processes": all_processes,
            "total_processes": len(all_processes)
        }