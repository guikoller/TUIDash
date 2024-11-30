# main.py

import sys
from Controller.system_controller import SystemController

def main():
    controller = SystemController()
    controller.run()

if __name__ == "__main__":
    main()