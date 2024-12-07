class ProcessView:
    def display_process_data(self, data):
        print("\n--- Processes ---")
        for process in data["processes"]:
            print(f"Process ID: {process['PID']}, Name: {process['Name']}, User: {process['User']}, Memory: {process['Memory']} KB, Status: {process['Status']}, RunTime: {process['RunTime']} seconds")
        print(data["total_processes"], "processes running")
            
            