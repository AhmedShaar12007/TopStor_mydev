import openpyxl
import subprocess

def read_excel(file_name="user_properties.xlsx"):
    # Load the Excel workbook
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active

    # Read the header row
    headers = [cell.value for cell in sheet[1]]
    
    # Initialize a list to store user data
    user_data = []

    # Iterate over the rows (starting from the second row)
    for row in sheet.iter_rows(min_row=2, values_only=True):
        user = dict(zip(headers, row))
        user_data.append(user)

    return user_data

def create_user_on_receiver(user_data):
    for user in user_data:
        username = user.get('name')
        encrypted_password = user.get('password')  # Assuming 'password' is the column name in the Excel
        groups = user.get('groups')  # Modify based on how groups are represented in your Excel

        # Check if user already exists
        user_check = subprocess.run(['id', username], capture_output=True, text=True)
        
        if user_check.returncode != 0:
            # User doesn't exist, create the user
            print(f"Creating user: {username}")
            user_add_command = ['sudo', 'useradd', '-m', '-p', encrypted_password, username]
            subprocess.run(user_add_command)

        # Create user groups (if groups exist)
        if groups:
            group_list = groups.split(',') if isinstance(groups, str) else [groups]

            for group in group_list:
                # Check if group exists
                group_check = subprocess.run(['getent', 'group', group], capture_output=True, text=True)
                if group_check.returncode != 0:
                    # Group doesn't exist, create the group
                    print(f"Creating group: {group}")
                    subprocess.run(['sudo', 'groupadd', group])

                # Add user to the group
                print(f"Adding user {username} to group {group}")
                subprocess.run(['sudo', 'usermod', '-aG', group, username])

def main():
    # Read user properties from the Excel file
    user_data = read_excel("user_properties.xlsx")
    
    if not user_data:
        print("No user data found in Excel.")
        return

    # Create users and groups on the receiver node
    create_user_on_receiver(user_data)

if __name__ == "__main__":
    main()

