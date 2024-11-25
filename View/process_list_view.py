# view/process_list_view.py

class ProcessListView:
    def update_processes(self, processes):
        """Update the process list view with the new processes."""
        if processes is None:
            print("Process data not available")
            return

        process_list = "PID    Name    User    CPU %    Memory (MB)\n"
        for proc in processes:
            process_list += (
                f"{proc['pid']}    {proc['name']}    {proc['username']}    "
                f"{proc['cpu_percent']}    {proc['memory_info'].rss // (1024 ** 2)}\n"
            )
        # print(process_list)