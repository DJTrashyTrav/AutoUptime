# AutoUptime
My senior project - a python script that polls a domain controller for a pc list, then reboots them if they haven't been restarted in a set time.

#Auto Uptime – System Manual
W. Travis Meeks – UAM – Fall 2024

#Goals and Objectives

In this class, I have decided to make a program that can be used by my work’s IT department to monitor uptime on domain computers, and have them reboot after a set threshold is met. There are a few things that I hope to be able to include, but am currently unsure of an implementation process for them. I’d like to first display a message warning the user that their computer will be rebooted before it actually happens. In tandem, I’d like to also have that reboot occur the following 2am, so that it is not an instant interruption for workers actively using the offending computer. The reason for 2am is that our main hospital EHR system reboots at 2am, so most night time users are aware that they may not be able to accomplish much at that time.

My goal for creating this system is to correct some often, yet random, occurrences of users calling our IT department to correct issues that are almost always solved by a simple reboot. I have tried to remind all users that “if nothing has changed, but something won’t work, it is usually corrected by a reboot.” They don’t retain that information very well at times, so this system will be a big help and a tremendous timesaver for my IT staff.

In the past, I have tried to correct this issue by deploying a GPO that will have all computers be forced to install windows updates at a set interval. I thought that would mean that all computers must be rebooted at that set interval; however, that was not the case. Sometimes there are no updates available to the computers for some time, which makes them not be forced to reboot. This program will be a more direct approach to fixing the problem, in lieu of relying on something else to force out the issue.

#Technical Specifications

This program is written in and dependent on the Python language. It has been written with variable user inputs to work in many different domain environments. For the most part, you will be able to follow the onscreen prompts to use the script appropriately. Dependencies will be listed below.

#Dependencies
•	Python – can be installed from the Microsoft store in Windows or preinstalled in most Linux environments
•	Imports – can be installed by running: “python pip install ldap3 wmi subprocess getpass colorama”
•	Domain Admin Credentials – Your credentials must have domain admin permissions
•	Connectivity to Domain - For this program to work, your terminal must be able to communicate with the domain controller and all domain computers.

#Development

#Program Narrative

Auto Uptime will allow a domain administrator to enter their domain information, administrator credentials, and custom uptime threshold to tailor the experience to match the desired outcome. This program will first poll a domain controller for a list of all PCs in the Computers OU container in the domain. This can be changed in the code of the program. It will then poll each computer in the list for their uptime, and cross reference it with the configured uptime threshold. If the computer has an uptime exceeding the defined threshold, it will configure a Windows Scheduled Task to both warn the user that their computer will reboot at midnight, and reboot the PC at midnight. The warning will pop up as a system notification at 1500. This can also be changed in the code of the program. If the uptime of the computer does not exceed the predefined threshold, you will see an output stating that the uptime of this computer is good.

#Troubleshooting
Outputs in the program have been color coded to make parsing easier for the user. Green means that the uptime is good. Yellow means the uptime was not good, but the reboot process was scheduled successfully. Red means that the uptime was not good and the reboot was unable to be scheduled. Connectivity problems will not change color, but will be output in the terminal. Connectivity problems for each computer do not necessarily mean there is a problem. As you know, not all domain computers are online at all times; most connectivity errors between your terminal and the domain computer are because the computer is offline. A tight firewall policy can also cause connectivity issues. This program relies on the domain computers having a punched hole for WinRM; it is very likely that your domain administrator already has this firewall hole in place. If not, look online for documentation on enabling it for your specific firewall or endpoint protection system.

#Sample Output

This picture shows a redacted version of live output against a domain. The lines that show Skipping a computer mean that computer was unavailable at the time of running the program. This is not uncommon in a domain environment. The Yellow line shows that a computer had an offending uptime and the reboot/warning was successfully scheduled. The green lines show that the computer’s uptime was okay.

![image](https://github.com/user-attachments/assets/5e407973-be00-4a8a-b8af-cbaa27c92a4e)
