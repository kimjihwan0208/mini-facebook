import socket
import sys
import getpass

try:
  #Address Family IPv4, Sock stream is TCP
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
  print("Failed to create socket. Error code: " + str(msg[0]) + " , Error message : " + msg[1])
  sys.exit()

print ("Socket Created")

#defining host and ip
host = '10.0.0.4'
port = 5050

#making tcp connection
s.connect( (host, port) ) #tuple of ip and port; tcp is a reliable pipe that connects 2 sockets

print ("Socket Connected to Server")

reply = s.recv(1858)
print(reply) #Welcome message

#log-in in a do-while loop fashion
username = raw_input("Username: ")
s.sendall(username)
exists_ack = s.recv(1)
while(exists_ack[0] == '0'):
	print("Please enter the correct username")
	username = raw_input("Username: ")
	s.sendall(username)
	exists_ack = s.recv(1)

password = getpass.getpass()
s.sendall(password)
auth_ack = s.recv(1)
while(auth_ack[0] == '0'):
	print("Please enter the correct password")
	password = getpass.getpass()
	s.sendall(password)
	auth_ack = s.recv(1)

#logged in
while(1):
	#display menu
	print("Menu\n1. Send Message\n2. Count Unread Message(s)\n3. Read Unread Message(s)\n4. Send Broadcast Messsage\n5. Change Password\n6. Logout\n---------------------------------------------------")
	#display received messages

	#get user's choice of action
	option = raw_input("Enter the number for the action: ")
	if (option == '5'):
		s.sendall("!p")
		#make sure old_pass is correct
		old_pwd = getpass.getpass(prompt="Old Password: ")
		s.sendall(old_pwd)
		ack = s.recv(1)
		while (ack == '0'):
			old_pwd = getpass.getpass(prompt="Old Password: ")
			s.sendall(old_pwd)
			ack = s.recv(1)
		#send new password and wait for server to confirm it	
		new_pwd = getpass.getpass("New Password: ")
		s.sendall(new_pwd)
		ack = s.recv(1)
		
		print("Password changed")
		
	elif (option == '6'):
		s.sendall("!q")
		break

'''
message = 'hi'
try:
  s.sendall(message) # sends the whole message
except socket.error:
  print("Send failed")
  sys.exit()
'''
#close socket
s.close()

