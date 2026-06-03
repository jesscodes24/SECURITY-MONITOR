import psutil
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CPU_THRESHOLD = 90 # CPU usage percentage threshold
MEMORY_THRESHOLD = 80 # Memory usage percentage threshold

def system_monitor():
   now = datetime.datetime.now()
   cpu = psutil.cpu_percent(interval=1)
   memory = psutil.virtual_memory().percent
   
   status = {
      "timestamp": now.strftime("%Y-%m-%d"),
      "date": now.strftime("%Y-%m-%d"),      #storing result of ze function
      "time": now.strftime("%H:%M:%S"),
      "cpu_usage": cpu,
      "memory_percentage": memory,
      "cpu_alert": cpu > CPU_THRESHOLD,
      "memory_alert": memory > MEMORY_THRESHOLD
    }
   
   return status

def display_health(status):
    print(f"Date: {status['timestamp']}")
    print(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"CPU Usage: {status['cpu_usage']}%")
    print(f"Memory Usage: {status['memory_percentage']}%")       # printt
   
    if status['cpu_alert']:
        print(" CPU usage is above recommended threshold!")
    if status['memory_alert']:
        print("Memory usage is above recommended threshold!")   



def log_book(status):
    with open("system_health_log", "a") as log_life:
        log_life.write(f"Date: {status['date']}\n")
        log_life.write(f"Time: {status['time']}\n")
        log_life.write(f"CPU Usage: {status['cpu_usage']}%\n")     #writing into log file 
        log_life.write(f"Memory Usage: {status['memory_percentage']}%\n")
        
        if status['cpu_alert']:
            log_life.write(" ALERT: CPU usage is above recommended threshold!\n")
        if status['memory_alert']:
            log_life.write(" ALERT: Memory usage is above recommended threshold!\n")
        log_life.write("-" * 40 + "\n")


def check_ip_reputation(ip_address, api_key):
    url = "https://api.abuseipdb.com/api/v2/check"
    
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
                                                             #
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)
    
    ip_data = data["data"]
    
    return {
        "ip": ip_address,
        "abuse_score": ip_data["abuseConfidenceScore"],
        "is_flagged": ip_data["abuseConfidenceScore"] > 50,
        "total_reports": ip_data["totalReports"],
        "country": ip_data["countryCode"]
    }



def display_ip_reputation(result):
    print(f"\n{'=' * 40}")
    print(" IP Reputation Check Result:")
    print(f"\n  IP Repution Check: {result['ip']}")
    print(f" Country: {result['country']}")
    print (f" Abuse score: {result['abuse_score']}/100")
    print(f" Total reports: {result['total_reports']}")
    print(f" Status: {' FLAGGED' if result['is_flagged'] else 'tick clean'}")                   #print again for ip reputation 
    print(f"\n{'=' * 40}")

def log_ip_reputation(result):
    with open("system_health_log", "a") as log_file:
        log_file.write(f"IP Check: {result['ip']}\n")
        log_file.write(f" Country: {result['country']}")
        log_file.write(f" Abuse score: {result['abuse_score']}/100")
        log_file.write(f" Total reports: {result['total_reports']}")
        log_file.write(f" Status: {' FLAGGED' if result['is_flagged'] else 'tick clean'}")
        log_file.write("-" * 40 +"\n")




if __name__ == "__main__":
    api_key = os.getenv("ABUSEIPDB_KEY")
    status = system_monitor()
    display_health(status)
    log_book(status)

    ip = input("\nEnter an IP address to check:")
    result =check_ip_reputation(ip, api_key)
    display_ip_reputation(result)
    log_ip_reputation(result)                 
