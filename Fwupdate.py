#!/usr/bin/python3
import sys
import time
from etcdget import etcdget as get
from etcdput import etcdput as put

def updatefw(data):
    """
    Description:
        Update the registry with the new update method that is identified in the data parameter.
    Parameter:
        data = dictionary. Example: { "updatemethod": "ftp", "updateloc": "ftp://xyz.com" }
    Action:
        - Puts the update key and value in the registry: ex. updatepls/ftp   ftp://xyz.com, using etcdput.
        - Puts the sync of the update value in the registry: ex. sync/updatepls/ftp/request  updatepls_stamp (where stamp is str(timestamp)).
        - Puts the sync of the update value in the registry: ex. sync/updatepls/ftp/request/leadername  updatepls_stamp (leadername is the name of the leader host like dchpxyz032).
    Return:
        - Dictionary example: {"result": "success"} if you read the value of the new key and find it using etcdget.
        - Or {"result": "fail"} if you cannot find it.
    """
    leaderip = "10.11.11.100"  # Placeholder, set it to an actual IP
    myhost = "owner"           # Placeholder, set it to an actual host

    # Debugging the input data
    print(f"Input data: {data}")

    # Extract parameters from data
    updatemethod = data.get("updatemethod")
    updateloc = data.get("updateloc")

    print(f"updatemethod: {updatemethod}, updateloc: {updateloc}")  # Debug values

    # Validate input
    if not updatemethod or not updateloc:
        print("failed - Missing updatemethod or updateloc")
        return {"result": "fail", "error": "Missing updatemethod or updateloc"}

    # Generate a timestamp string
    timestamp_str = str(int(time.time()))  # Convert the time to an integer timestamp
    print(f"Timestamp: {timestamp_str}")  # Debug timestamp

    # Registry updates with logging
    log_put(leaderip, f"updatepls/{updatemethod}", updateloc)
    log_put(leaderip, f"sync/updatepls/{updatemethod}/request", f"updatepls_{timestamp_str}")
    log_put(leaderip, f"sync/updatepls/{updatemethod}/request/{myhost}", f"updatepls_{timestamp_str}")
   # log_put(leaderip, f"sync/updatepls/{updatemethod}/request/leadername", "sync")

    # Verify the registry updates using etcdget
    fetched_value = get(leaderip, f"updatepls/{updatemethod}")
    print(f"Fetched value: {fetched_value}")  # Debug fetched value

    if fetched_value and fetched_value[0] == updateloc:
        print("Update successful")
        return {"result": "success"}
    else:
        print("Update failed - Could not verify the value in the registry")
        return {"result": "fail", "error": "Registry update verification failed"}

def log_put(etcd, key, value):
    """
    A wrapper for the etcdput function that logs actions in the format:
    - key: value
    """
    print(f"Putting key: {key}, value: {value}")
    put(etcd, key, value)

# Ensure updatefw() is called with the correct data
if __name__ == "__main__":  # Ensure the code runs only if the script is executed directly
    data = {"updatemethod": "ftp", "updateloc": "ftp://xyz.com"}
    print(f"Calling updatefw() with data: {data}")
    result = updatefw(data)
    print(f"Result: {result}")

