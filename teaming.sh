# Team Interface Configuration
TEAM_INTERFACE="team0"
TEAM_CONFIG='{"runner": {"name": "activebackup"}}'

# Use the detected interfaces for teaming
PHYSICAL_INTERFACES=("${eth_list[@]}")

# Step 1: Remove existing team interface (if any)
echo "Removing existing team interface $TEAM_INTERFACE (if any)..."
nmcli conn delete $TEAM_INTERFACE 2>/dev/null

# Step 2: Create the team interface
echo "Creating team interface $TEAM_INTERFACE..."
nmcli conn add con-name $TEAM_INTERFACE type team ifname $TEAM_INTERFACE config "$TEAM_CONFIG"

# Step 3: Configure IP address and gateway dynamically
echo "Detecting current node IP..."
mynode=$(ip -4 addr show | awk '/inet / {print $2}' | head -n 1)
echo "Configuring IP address $mynode on $TEAM_INTERFACE..."
nmcli conn modify $TEAM_INTERFACE ipv4.addresses $mynode
nmcli conn modify $TEAM_INTERFACE ipv4.method manual

# Step 4: Add physical interfaces as slaves to the team interface
count=1
for interface in "${PHYSICAL_INTERFACES[@]}"; do
    echo "Adding $interface as a slave to $TEAM_INTERFACE..."
    nmcli conn add con-name $TEAM_INTERFACE-port$count type team-slave ifname $interface master $TEAM_INTERFACE
    count=$((count+1))
done

# Step 5: Bring up the team interface and its slaves
echo "Bringing up $TEAM_INTERFACE and its slaves..."
nmcli conn up $TEAM_INTERFACE
count=1
for interface in "${PHYSICAL_INTERFACES[@]}"; do
    nmcli conn up $TEAM_INTERFACE-port$count
    count=$((count+1))
done

# Step 6: Verify the configuration
echo "Verifying team interface configuration..."
teamdctl $TEAM_INTERFACE state
ip addr show $TEAM_INTERFACE

echo "Team interface setup complete!"

