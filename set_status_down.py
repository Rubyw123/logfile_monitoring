import requests
import os

def get_ip():
    ip = requests.get("https://httpbin.org/ip")
    return ip.json(['origin'])

def update_server_status(status,ip):
    db_url = 'https://avmtlbxffksxidupbiel.supabase.co/rest/v1/server_stats' 
    headers = {
        "Content-Type": "application/json",
        "apikey": os.environ.get("SUPABASE_LOG_SERVICE_KEY"),
        "Authorization": "Bearer "+os.environ.get("SUPABASE_LOG_SERVICE_KEY"),
        "Prefer": "resolution=merge-duplicates",

    }
    data={
        "server_ip":ip,
        "status":status,
    }

    response = requests.post(db_url, json=data, headers = headers)
    
    print(db_url+"?server_ip=eq."+ip)
    if response.status_code == 200:
        print("Success")
    else:
        print("Error:",response.text)

if __name__ == "__main__":

    ip = get_ip()

    update_server_status(False,ip)