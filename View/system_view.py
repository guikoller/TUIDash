import os
import datetime

class SystemView:
    def display_system_data(self, data):
        self.clear_console()
        print("\n" + "=" * 40)
        print("System Information:")
        print("=" * 40)
        print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 40)
        
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            elif isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")

    def clear_console(self):
        os.system('clear' if os.name == 'posix' else 'cls')