import win32com.client
import datetime
import ldap3
import wmi
import subprocess
import getpass
from colorama import Fore, Style

def get_domain_computers(dc_address, username, password, domain_name, domain_ext):
    """Retrieves a list of domain computers using LDAP3."""
    server = ldap3.Server(dc_address)
    conn = ldap3.Connection(server, user=domain_name + "\\" + username, password=password)

    if conn.bind():
        # Construct the search base dynamically based on user input
        search_base = f"CN=Computers,DC={domain_name},DC={domain_ext}"
        if conn.search(search_base=search_base,
                       search_filter="(objectClass=computer)",
                       attributes=["name", "operatingSystem"]):
            entries = [entry for entry in conn.entries]  # Convert entries to a list
            return entries if entries else []  # Return empty list if no entries
    else:
        print("Failed to bind to LDAP server.")
        return []  # Return an empty list on failure.

def get_computer_uptime(computer_name):
    """Gets the uptime of a specific computer using WMI. Handles potential x_wmi exceptions."""
    try:
        wmi_obj = wmi.WMI(computer=computer_name)
        for win32_perf_formatted_data in wmi_obj.Win32_PerfFormattedData_PerfOS_System():
            uptime_seconds = int(win32_perf_formatted_data.SystemUpTime)
            total_minutes = uptime_seconds // 60
#            print(f"{computer_name}'s uptime is {total_minutes} minutes...") # only for testing.
            return total_minutes
    except Exception as e:
        raise WMIError(f"WMI error for {computer_name}: {e}")  # Raise a custom WMIError exception

    except Exception as e:
        print(f"Unexpected error for {computer_name}: {e}")
    return None  # Indicate failure to retrieve uptime

class WMIError(Exception):
    pass  # Create a custom exception class for WMI errors

def schedule_reboot_with_schtasks(computer_name, domain_name, username, password):
  """Schedules a one-time reboot at midnight using schtasks."""
  command = "shutdown /r /f /t 32400 /c 'Your computer will reboot at midnight. -Trav'"
  schtasks_command = f'schtasks /create /s {computer_name} /u {domain_name}\\{username} /p {password} /tn "Midnight Reboot" /sc ONCE /st "14:59" /tr "{command}"'
#  print(f"Running command: {schtasks_command}") # only for testing syntax.
  result = subprocess.run(schtasks_command, shell=True, capture_output=True, text=True)
  
  if result.returncode == 0:
    print(f"{Fore.YELLOW}!!! Scheduled reboot for {computer_name} at midnight{Style.RESET_ALL}")
  else:
    print(f"{Fore.RED}--- Failed to schedule reboot for {computer_name}: {result.stderr}{Style.RESET_ALL}")
        

def main():
    # Get user-defined threshold
    threshold = int(input("Enter the uptime threshold (in minutes): "))

    # Get LDAP credentials and domain name from the user
    dc_address = input("Enter the domain controller address: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    domain_name = input("Enter the domain name (minus the .org): ")
    domain_ext = input("Enter your domain extension (org, com, etc): ")

    # Get domain computers
    computers = get_domain_computers(dc_address, username, password, domain_name, domain_ext)

    # Check for successful LDAP bind (assuming empty list on failure)
    if not computers:
        print("Failed to retrieve computers. Please check credentials or network connectivity.")
        return  # Exit the program

    # Check uptime for each computer
    for computer in computers:
      try:
        uptime = get_computer_uptime(computer["name"])
        if uptime is not None and uptime > threshold:
          schedule_reboot_with_schtasks(computer["name"], domain_name, username, password)
        else:
          print(f"{Fore.GREEN}=== {computer['name']}'s uptime is good!{Style.RESET_ALL}")
      except WMIError as e:
        print(f"Skipping {computer['name']}")


if __name__ == "__main__":
    main()