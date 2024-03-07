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

def update_server_status(status,ip,logfile):
    db_url = 'https://avmtlbxffksxidupbiel.supabase.co/rest/v1/server_stats' 
    # TODOS: Hard coded apikeys for now. Need solve security later.
    headers = {
        "Content-Type": "application/json",
        #"apikey": os.environ.get("SUPABASE_LOG_SERVICE_KEY"),
        "apikey":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF2bXRsYnhmZmtzeGlkdXBiaWVsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwOTMyNDE3MiwiZXhwIjoyMDI0OTAwMTcyfQ.5bwX_GojbxArhz0xlqKZ4ih6s1Wwf80LiPnwftsZwS0",
        #"Authorization": "Bearer "+os.environ.get("SUPABASE_LOG_SERVICE_KEY"),
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF2bXRsYnhmZmtzeGlkdXBiaWVsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwOTMyNDE3MiwiZXhwIjoyMDI0OTAwMTcyfQ.5bwX_GojbxArhz0xlqKZ4ih6s1Wwf80LiPnwftsZwS0",
        "Prefer": "resolution=merge-duplicates",

    }
    data={
        "server_ip":ip,
        "status":status,
    }

    #APi call
    response = requests.post(db_url, json=data, headers = headers)
    
    if response.status_code == 200:
        print("Successfully Update DB Status!",file=logfile,flush=True)
    else:
        print("Error:",response.text,file=logfile,flush=True)


if __name__ == "__main__":
    #Capturing system output
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
    while True:
        try:
            #Open logfile
            with open('/home/srv1/Documents/logfile_monitoring/output/out_python.log','a') as logfile:
                # Read input log entry and write to logfile
                inputline = sys.stdin.readline()
                print(f"Input Log Entry:{inputline.strip()}",file=logfile,flush=True)


                #Setting server status
                ip = get_ip()
                print(f"Server Ip: {ip.strip()}", file=logfile, flush=True)

                #Test Environment Variables
                #key = os.environ.get("SUPABASE_LOG_SERVICE_KEY")
                #print(f"Key variable completed: {key.strip()}", file=logfile, flush=True)

                #Set Status as Up(True)
                update_server_status(True,ip,logfile)
                print(f"Server Side Completed", file=logfile, flush=True)

                logfile.flush()
                #sys.stdout = original_stdout

            #Set the permissions of logfile
            os.chmod(logfile,0o666)
            
        except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)
                sys.stderr.flush()


