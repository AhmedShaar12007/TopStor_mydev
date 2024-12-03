import ipaddress
import logging

# Configure logging
logging.basicConfig(filename='/var/log/TopStor_fapi.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_ip(ip):
    """
    Validate if the given IP address is in a valid format.
    Args:
        ip (str): IP address as a string.
    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def process_ip(ip, action):
    """
    Validate and process IP-related actions (e.g., CIFS, NFS, ISCSI, etc.).
    Args:
        ip (str): IP address as a string.
        action (str): Action type (e.g., "CIFS", "NFS", "ISCSI").
    """
    if not is_valid_ip(ip):
        error_message = f"Invalid IP address: {ip}. No changes made for {action}."
        print(error_message)
        logging.error(error_message)
        return False
    # Proceed with the required action
    logging.info(f"Processing {action} for IP: {ip}")
    return True

# Example usage within the main script
def create_cifs(ip, other_params):
    if not process_ip(ip, "CIFS"):
        return
    # Continue with CIFS creation logic

def create_nfs(ip, other_params):
    if not process_ip(ip, "NFS"):
        return
    # Continue with NFS creation logic

def create_iscsi(ip, other_params):
    if not process_ip(ip, "ISCSI"):
        return
    # Continue with ISCSI creation logic

def create_user_home(ip, username):
    if not process_ip(ip, "User Home Folder"):
        return
    # Continue with user home folder logic

