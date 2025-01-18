#!/usr/bin/python3
import sys
import time
import subprocess
import os

# Function to interact with etcd using etcdctl command-line tool
def etcdctl(etcd, key, value):
    cmdline = ['etcdctl', '--user=root:YN-Password_123', '--endpoints=http://' + etcd + ':2379', 'put', key, value]
    try:
        result = subprocess.run(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        if result.returncode == 0:
            return True  # Success
        else:
            print(f"Error: {result.stderr.decode()}")
            return False  # Failure
    except Exception as e:
        print(f"Error while running etcdctl: {e}")
        return False  # Failure


# Function to call etcdctl through a wrapper
def etcdput(etcd, key, value):
    os.environ['ETCDCTL_API'] = '3'  # Make sure we're using etcd API v3
    return etcdctl(etcd, key, value)


def updatefw(data):
    leaderip = "10.11.11.100"  # Placeholder for the leader IP
    myhost = "owner"           # Placeholder for the host name
    timestamp_str = str(int(time.time()))  # Generate a timestamp string
    print(f"Timestamp: {timestamp_str}")  # Debug timestamp

    updatemethod = data.get("updatemethod")
    updateloc = data.get("updateloc")

    if not updatemethod or not updateloc:
        print("failed - Missing updatemethod or updateloc")
        return {"result": "fail", "error": "Missing updatemethod or updateloc"}

    # Write the keys to etcd using the modified put function (etcdput)
    if not etcdput(leaderip, f"sync/updatepls/{updatemethod}/request", f"updatepls_{timestamp_str}_{leaderip}"):
        print("Failed to write key to etcd")
        return {"result": "fail", "error": "Failed to write key"}
    
    if not etcdput(leaderip, f"sync/updatepls/{updatemethod}/request/{myhost}", f"updatepls_{timestamp_str}_{leaderip}"):
        print("Failed to write key to etcd")
        return {"result": "fail", "error": "Failed to write key"}
    
    if not etcdput(leaderip, f"sync/updatepls/{updatemethod}/request/leader", "sync"):
        print("Failed to write key to etcd")
        return {"result": "fail", "error": "Failed to write key"}

    return {"result": "success"}


# Main script execution
if __name__ == "__main__":
    data = {"updatemethod": "ftp", "updateloc": "ftp://xyz.com"}
    print(f"Calling updatefw() with data: {data}")
    result = updatefw(data)
    print(f"Result: {result}")

