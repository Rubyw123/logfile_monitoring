#!/usr/bin/python3
# encoding:utf-8

import requests
import os
import json
import subprocess
import sys


def get_ip():
    status_data = subprocess.check_output(["tailscale", "status", "--json"]).decode("utf-8")
    status_data = json.loads(status_data)

    return status_data["TailscaleIPs"][0]

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
    while True:
        log_entry = sys.stdin.readline()
        output = sys.stdout.readline()
        error = sys.stderr.readline()

        file = open("/home/srv1/Documents/logfile_monitoring/output/out_python.log","a")
        file.write(log_entry)

        ip = get_ip()
        update_server_status(True,ip)

        file.write(output)
        file.write(error)
        file.close()


