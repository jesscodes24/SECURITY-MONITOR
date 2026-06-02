
import psutil
import datetime

CPU_THRESHOLD = 90 # CPU usage percentage threshold
MEMORY_THRESHOLD = 80 # Memory usage percentage threshold

def system_monitor():
   now = datetime.datetime.now()
   cpu = psutil.cpu_percent(interval=1)
   memory = psutil.virtual_memory().percent
   
   status = {
      "timestamp": now.strftime("%Y-%m-%d"),
      "date": now.strftime("%Y-%m-%d"),
      "time": now.strftime("%H:%M:%S"),
      "cpu_usage": cpu,
      "memory_percentage": memory,
      "cpu_alert": cpu > CPU_THRESHOLD,
      "memory_alert": memory > MEMORY_THRESHOLD
    }
   
   return status

def display_health_(status):
    print(f"Timestamp: {status['timestamp']}")
    print(f"Date: {status['timestamp']}")
    print(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"CPU Usage: {status['cpu_usage']}%")
    print(f"Memory Usage: {status['memory_percentage']}%")
   
    if status['cpu_alert']:
        print(" CPU usage is above recommended threshold!")
    if status['memory_alert']:
        print("Memory usage is above recommended threshold!")   



def log_book(status):
    with open("system_health_log", "a") as log_life:
        log_life.write(f"Date: {status['date']}\n")
        log_life.write(f"Time: {status['time']}\n")
        log_life.write(f"CPU Usage: {status['cpu_usage']}%\n")
        log_life.write(f"Memory Usage: {status['memory_percentage']}%\n")
        
        if status['cpu_alert']:
            log_life.write(" ALERT: CPU usage is above recommended threshold!\n")
        if status['memory_alert']:
            log_life.write(" ALERT: Memory usage is above recommended threshold!\n")
        log_life.write("-" * 40 + "\n")


if __name__ == "__main__":
    status = system_monitor()
    display_health_(status)
    log_book(status)

