# main.py

import time
from Controller.dashboard_controller import DashboardController

def main():
    controller = DashboardController()
    try:
        while True:
            # Debugging statements to check if threads are running
            print(f"CollectThread is alive: {controller.collect_thread.is_alive()}")
            print(f"ProcessThread is alive: {controller.process_thread.is_alive()}")

            # Check if there is processed data to display
            if not controller.process_to_display_queue.empty():
                data = controller.process_to_display_queue.get()
                controller.dashboard_view.update_system_info(data)
                controller.dashboard_view.update_process_list(data["processes"])

            time.sleep(5)  # Print the information every 5 seconds
    except KeyboardInterrupt:
        controller.running = False
        controller.collect_thread.join()
        controller.process_thread.join()

if __name__ == "__main__":
    main()