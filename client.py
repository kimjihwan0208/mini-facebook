import socket
import sys
import getpass
import select

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
#s.setblocking(0)
numUnread = s.recv(1024)
print("# of Unread Messages: " + numUnread)
while(1):
    #display menu
	print("Menu\n1. Send Message\n2. Send Friend Request\n3. Read Unread Message(s)\n4. Send Broadcast Messsage\n5. Change Password\n6. Logout\n---------------------------------------------------")
	
	ready = select.select([s], [], [], 3)
	while(ready[0]):
		data = s.recv(4096)
		print(data)
		ready = select.select([s], [], [], 3)
	
	#get user's choice of action
	option = raw_input("Enter the number for the action: ")
	
	if (option == '1'): #send message
		s.sendall("!sendone")
		receiver = raw_input("Enter receiver: ")
		s.sendall(receiver)
		msg = raw_input("Enter message: ")
		s.sendall(msg)
		ack = s.recv(1)
		print("Message sent")
		
	elif (option == '2'): #Send Friend Request
		continue
		
	elif (option == '3'): #read unread message
		s.sendall("!readall")
		unread_msg = s.recv(1024)
		while(unread_msg[0:2] != '!x'):
			print(unread_msg)
			unread_msg = s.recv(1024)
		print("-----------\nNo More Unread Messages!")
		
	elif (option == '4'): #broadcast message to everyone online
		s.sendall("!sendall")
		msg = raw_input("Enter message: ")
		s.sendall(msg)
		ack = s.recv(1)
		print("Message sent")
		
	elif (option == '5'):
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
	
	else:
		continue

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

