import paramiko
import sys
import getpass

list = [] # define a list for cd commands
def MainConnection():
	if (len(sys.argv) == 2): #if only python, website
		sshAddress = sys.argv[1]
		sshUsername = input("Username: ") #need username
	elif (len(sys.argv) == 3): #if python, website, username
		sshAddress = sys.argv[1]
		sshUsername = sys.argv[2]
	else:
		#No arg given for website ask for it here
		sshAddress = input("SSH Connection: ")
		print("Connecting to: ", sshAddress)
		#Get username and password variables
		sshUsername = input("Username: ")
	#Always going to need to ask for password
	sshPassword = getpass.getpass("Password: ")
	SshConnect(sshAddress, sshUsername, sshPassword)
	
#function to connect via SSH
def SshConnect(sshAdd, sshUser, sshPass):
	commContinue = True; # loop condition to continue accepting commands
	cd = False; # If a cd command has been given
	pathChange = True; # If the path needs to be changed
	#SSH connecting
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(sshAdd, username=sshUser, 
	password=sshPass)
	print("Success connected to: " + sshAdd + " as: " + sshUser)
	
	# Continually ask for commands
	while (commContinue == True):
		if (pathChange == True):
			# Prints out the path ex C:\Users\Python >> 
			tempString = ""
			for items in list:
				tempString += items + ";"
			pathChange = False
			stdin, stdout, stderr = ssh.exec_command(tempString + "pwd")
			path = stdout.read().decode(encoding='UTF-8').strip()
			command = input(path + " >> ")
		else:
			# Speed up not having to check each time if no cd has been made.
			# Allows for faster performance
			command = input(path + " >> ")
		if (command == "exit"):
			# Exit the ssh
			commContinue = False
		else:
			# Add the cd command to a list
			# Doing this due to exec_command to be a single instance
			if (command.startswith("cd")):
				list.append(command)
				pathChange = True
				tempString = ""
				for num in list:
					tempString += num + ";"
				cd = True
				stdin, stdout, stderr = ssh.exec_command(tempString)
				# convert the stdout to a string
				temp = stdout.read().decode(encoding='UTF-8')
			elif (cd == True):
				# Check if a text editor is called
				if (command.startswith("vi") or command.startswith("emacs") or command.startswith("vim") or command.startswith("nano")):
					print("cannot use editor: ")
				else:
					# if cd is true and no editor command given
					tempString = ""
					for num in list:
						tempString += num + ";"
					stdin, stdout, stderr = ssh.exec_command(tempString + command)
					temp = stdout.read().decode(encoding='UTF-8')
					print(temp)
			elif (command.startswith("vi") or command.startswith("emacs") or command.startswith("vim") or command.startswith("nano")):
				print("cannot use editor: ")
			else: # if cd has never been called
				stdin, stdout, stderr = ssh.exec_command(command)
				temp = stdout.read().decode(encoding='UTF-8')
				print(temp)
	ssh.close()
MainConnection()