#!/bin/bash

# Variables
TEAM_INTERFACE="team0"
TEAM_IP="10.12.12.10/24"
TEAM_GATEWAY="10.12.12.1"
PHYSICAL_INTERFACES=("enp0s10" "enp0s9")
TEAM_CONFIG='{"runner": {"name": "activebackup"}}'

# Step 1: Disable IP addresses on physical interfaces
#for interface in "${PHYSICAL_INTERFACES[@]}"; do
   # echo "Disabling IP on $interface..."
   # sudo nmcli connection modify "$interface" ipv4.method disabled
#done

# Step 2: Remove existing team interface (if it exists)
#echo "Removing existing team interface $TEAM_INTERFACE (if any)..."
#sudo nmcli connection delete "$TEAM_INTERFACE" 2>/dev/null

# Step 3: Create the team interface
echo "Creating team interface $TEAM_INTERFACE..."
nmcli connection add type team con-name $TEAM_INTERFACE ifname $TEAM_INTERFACE config '{"runner": {"name": "activebackup"}}'

# Step 4: Clear any existing IP and gateway configuration
#echo "Clearing existing IP and gateway configuration on $TEAM_INTERFACE..."
#nmcli connection modify $TEAM_INTERFACE ipv4.addresses ""
#nmcli connection modify $TEAM_INTERFACE ipv4.gateway ""

# Step 5: Assign new IP address and gateway to the team interface
echo "Configuring IP address $TEAM_IP and gateway $TEAM_GATEWAY on $TEAM_INTERFACE..."
nmcli connection modify $TEAM_INTERFACE ipv4.addresses $TEAM_IP
nmcli connection modify $TEAM_INTERFACE ipv4.gateway $TEAM_GATEWAY
nmcli connection modify $TEAM_INTERFACE ipv4.method manual
count=1
# Step 6: Add physical interfaces as slaves to the team interface
for interface in "${PHYSICAL_INTERFACES[@]}"; do
    echo "Adding $interface as a slave to $TEAM_INTERFACE..."
    nmcli connection add type team-slave con-name $TEAM_INTERFACE-port$count ifname $interface master $TEAM_INTERFACE    
    count=$((count+1))
done

# Step 7: Bring up the team interface and its slaves
echo "Bringing up $TEAM_INTERFACE and its slaves..."
sudo nmcli connection up $TEAM_INTERFACE
count=1
for interface in "${PHYSICAL_INTERFACES[@]}"; do
    nmcli connection up $TEAM_INTERFACE-port$count
    count=$((count+1))
done

# Step 8: Verify the configuration
echo "Verifying team interface configuration..."
teamdctl $TEAM_INTERFACE state
ip addr show $TEAM_INTERFACE

echo "Team interface setup complete!"
