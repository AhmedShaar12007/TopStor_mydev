#!/usr/bin/python3
import time  # Ensure this is imported
from etcdget import etcdget as get  # Confirm the module path is correct
from etcdput import etcdput as put  # Confirm the module path is correct

def updatefw(data):
    """
    Updates etcd registry with the provided update method and location.

    Args:
        data (dict): Contains 'updatemethod' and 'updateloc'.
                     Example: {'updatemethod': 'ftp', 'updateloc': 'ftp://xyz.com'}

    Returns:
        dict: Result of the operation. {"result": "success"} or {"result": "fail", "error": "reason"}
    """
    leaderip = "10.11.11.100"  # Replace with actual etcd leader IP
    myhost = "owner"           # Replace with actual host name

    # Debugging the input data
    print(f"Input data: {data}")

    # Extract required parameters
    updatemethod = data.get("updatemethod")
    updateloc = data.get("updateloc")

    # Validate input
    if not updatemethod or not updateloc:
        print("Failed - Missing 'updatemethod' or 'updateloc'")
        return {"result": "fail", "error": "Missing 'updatemethod' or 'updateloc'"}

    # Generate a timestamp
    timestamp_str = str(int(time.time()))
    print(f"Generated timestamp: {timestamp_str}")

    # Write keys to etcd
    success1 = put(leaderip, f"sync/updatepls/{updatemethod}/request", f"updatepls_{timestamp_str}_{leaderip}")
    success2 = put(leaderip, f"sync/updatepls/{updatemethod}/request/{myhost}", f"updatepls_{timestamp_str}_{leaderip}")
    success3 = put(leaderip, f"sync/updatepls/{updatemethod}/request/leader", "sync")

    # Check if all keys were successfully written
    if success1 and success2 and success3:
        print("All keys written successfully")
        return {"result": "success"}
    else:
        # Identify which key failed
        errors = []
        if not success1:
            errors.append(f"Failed to write key sync/updatepls/{updatemethod}/request")
        if not success2:
            errors.append(f"Failed to write key sync/updatepls/{updatemethod}/request/{myhost}")
        if not success3:
            errors.append(f"Failed to write key sync/updatepls/{updatemethod}/request/leader")

        error_message = "; ".join(errors)
        print(error_message)
        return {"result": "fail", "error": error_message}

if __name__ == "__main__":
    # Example input data
    data = {"updatemethod": "ftp", "updateloc": "ftp://xyz.com"}

    # Call the updatefw function and print the result
    print(f"Calling updatefw() with data: {data}")
    result = updatefw(data)
    print(f"Result: {result}")

