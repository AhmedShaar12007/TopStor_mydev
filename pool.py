# Read the file content
file_path = '/mnt/data/pool_status (2).txt'
with open(file_path, 'r') as file:
    data = file.read()

# Initialize variables
pools = []
pool_info = {}
lines = data.splitlines()

# Parse the file line by line
for line in lines:
    if line.startswith('pool:'):
        # Start a new pool entry
        if pool_info:
            pools.append(pool_info)
        pool_name = line.split(':')[1].strip()
        pool_info = {'pool': pool_name, 'status': 'normal'}
    elif line.startswith('  scan:'):
        if 'resilvering' in line:
            pool_info['status'] = 'resilvering'
        elif 'resilvered' in line:
            pool_info['status'] = 'resilvered'

# Append the last pool
if pool_info:
    pools.append(pool_info)

# Output the list of dictionaries
print(pools)

