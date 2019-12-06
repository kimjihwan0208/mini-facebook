import socket
import sys
from thread import *

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #dummy socket object
user_list = {"amy":["apass",0,"",s2, [ ]],"bob":["bpass",0,"",s2,[ ]],"cat":["cpass",0,"",s2,[ ]]}

def clientthread(conn,ip): #each clientthread for each client. lasts until client logs out
	#sending message to connected client
	conn.send("Welcome to mini-facebook. Please Log In")
  
	#username authentication
	exists = False
	user = conn.recv(10)
	for u in user_list:
		if u == user:
			exists = True
			conn.send("1")
			break
	while (not exists):
		conn.send("0")
		user = conn.recv(10)
		for u in user_list:
			if u == user:
				exists = True
				conn.send("1")
				break
  
	#password authentication
	auth = False
	pwd = conn.recv(1024)
	for u in user_list:
		if (u == user and user_list[user][0] == pwd):
			auth = True
			conn.send("1")
			break
	while(not auth):
		conn.send("0")
		pwd = conn.recv(1024)
		for u in user_list:
			if (u == user and user_list[user][0] == pwd):
				auth = True
				conn.send("1")
				break
	user_list[user][1] = 1
	user_list[user][2] = ip
	user_list[user][3] = conn
	
	print(user + " is now online on ip: " + ip)
	#logged in
	conn.send(str(len(user_list[user][4]))) #unread count
	while True:
		data = conn.recv(1024)
		if data[0:2] == "!q" :
			break
      
		elif data[0:8] == "!sendone":
			send_to = conn.recv(1024)
			msg = conn.recv(1024)
			if user_list[send_to][1]:
				user_list[send_to][3].send(msg)
			else:
				user_list[send_to][4].append(msg)
			conn.send('1')
		
		elif data[0:8] == "!readall":
			while len(user_list[user][4]) != 0:
				conn.sendall(user_list[user][4][0])
				print(user_list[user][4][0])
				user_list[user][4].pop(0)

			conn.sendall('!x')
	  
		elif data[0:2] == "!p" :
			#check old password
			old_pwd = conn.recv(1024)
			while (user_list[user][0] != old_pwd):
				conn.send('0')
				old_pwd = conn.recv(1024)
			conn.send('1') #correct old password, send ack 1
			#receive and change to new password
			new_pwd = conn.recv(1024)
			user_list[user][0] = new_pwd;
			conn.send('1') #good to go ack
			
		elif data[0:8] == "!sendall":
			msg = conn.recv(1024)
			for u in user_list:
				if user_list[u][1] and u != user:
					#print(u)
					user_list[u][3].send(msg)
			conn.send('1')
		else:
		  #conn.sendall(reply)
			continue

	conn.close()
	user_list[user][1] = 0
	user_list[user][2] = ''
	user_list[user][3] = s2
	print(user + " logged out")


Host = "" #all available interfaces
Port = 5050 #random number

#creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print ("socket created")

#binding socket
try:
  s.bind((Host, Port)) #tuple again
except socket.error as msg:
  print ("Bind failed. Error code: " + str(msg[0]) + "Message: " +str(msg[1]))
  sys.exit()

print("socket bind complete")

#listening
s.listen(10) #10 is the backlog; number of incoming connections that can wait; 11th will be rejected
print("socket now listening")

#send message back to client
while 1:
  conn, addr = s.accept() #conn is the socket object and addr is ip:port
  print("Connected with " + addr[0] + ":" + str(addr[1]))
  
  start_new_thread(clientthread, (conn,addr[0]))

s.close()

