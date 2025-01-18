def updatefw(data):
    leaderip = "10.11.11.100"  # Placeholder, set it to an actual IP
    myhost = "owner"           # Placeholder, set it to an actual host

    # Debugging the input data
    print(f"Input data: {data}")

    updatemethod = data.get("updatemethod")
    updateloc = data.get("updateloc")

    if not updatemethod or not updateloc:
        print("Failed - Missing updatemethod or updateloc")
        return {"result": "fail", "error": "Missing updatemethod or updateloc"}

    timestamp_str = str(int(time.time()))
    print(f"Timestamp: {timestamp_str}")

    # Write keys to etcd
    success1 = put(leaderip, f"sync/updatepls/{updatemethod}/request", f"updatepls_{timestamp_str}_{leaderip}")
    success2 = put(leaderip, f"sync/updatepls/{updatemethod}/request/{myhost}", f"updatepls_{timestamp_str}_{leaderip}")
    success3 = put(leaderip, f"sync/updatepls/{updatemethod}/request/leader", "sync")

    if success1 and success2 and success3:
        print("All keys written successfully")
        return {"result": "success"}
    else:
        print("One or more keys failed to write")
        return {"result": "fail", "error": "Failed to write keys"}

if __name__ == "__main__":  # Ensure the script is being run directly
    # Example input data
    data = {"updatemethod": "ftp", "updateloc": "ftp://xyz.com"}
    
    # Call the updatefw function with the data
    print(f"Calling updatefw() with data: {data}")
    result = updatefw(data)
    print(f"Result: {result}")

