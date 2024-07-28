import time
import random
import os
from datetime import datetime

# List of simulated data
ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
methods = ["GET", "POST"]
urls = ["/home", "/login", "/register", "/data"]
statuses = [200, 404, 500]
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]
LOG_FILE = "/app/logs/web_server_logs.csv"
LOG_FILE_SIZE_LIMIT = 5 * 1024 * 1024  # 5 MB

def generate_log():
    ip = random.choice(ips)
    method = random.choice(methods)
    url = random.choice(urls)
    status = random.choice(statuses)
    user_agent = random.choice(user_agents)
    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S %z")
    log_entry = f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} - "-" "{user_agent}"\n'
    return log_entry

def rotate_log_file():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    os.rename(LOG_FILE, f"/app/log_generator/logs/web_server_logs_{timestamp}.csv")

if __name__ == "__main__":
    while True:
        log = generate_log()
        print(log.strip())  # Print to console for testing
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > LOG_FILE_SIZE_LIMIT:
            rotate_log_file()
        with open(LOG_FILE, "a") as f:
            f.write(log)
        time.sleep(0.5)  # Simulate a delay between log entries