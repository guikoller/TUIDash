import os
import pwd

class ProcessModel:
    def get_process_list(self, page=1, processes_per_page=20):
        processes = []
        all_processes = []
        try:
            # Gather all processes
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

                        all_processes.append({
                            "PID": pid,
                            "Name": stat_data[1].strip("()"),
                            "User": user,
                            "Memory": memory_usage or "N/A"
                        })

            # Calculate pagination
            total_processes = len(all_processes)
            total_pages = (total_processes + processes_per_page - 1) // processes_per_page
            page = max(1, min(page, total_pages))  # Clamp page number within bounds
            start_index = (page - 1) * processes_per_page
            end_index = start_index + processes_per_page

            # Get the processes for the current page
            processes = all_processes[start_index:end_index]
        except Exception as e:
            print(f"Error reading processes: {e}")

        return {
            "processes": processes,
            "total_processes": len(all_processes),
            "total_pages": total_pages,
            "current_page": page,
        }
