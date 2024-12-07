class SystemView:
    def display_cpu_info(self, cpu_info, usage):
        print("CPU Info:")
        for key, value in cpu_info.items():
            print(f"{key}: {value}")
        print(f"CPU Usage: {usage}%\n")

    def display_memory_info(self, memory_info, usage):
        print("Memory Info:")
        for key, value in memory_info.items():
            print(f"{key}: {value}")
        print(f"Memory Usage: {usage}%\n")
    
    def display_system_data(self, data):
        self.display_cpu_info(data["CPU Info"], data["CPU Usage"])
        self.display_memory_info(data["Memory Info"], data["Memory Usage"])
