# bot_runner.py

import time
import os

while True:
    print("\n🚀 Launching main.py...\n")
    os.system("python3 main.py")
    
    print("\n🔁 Waiting 10 minutes before next run...\n")
    time.sleep(600)  # 600 seconds = 10 minutes
