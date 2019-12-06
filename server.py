import socket
import sys
from thread import *

user_list = {"amy":["apass",0,""],"bob":["bpass",0,""],"cat":["cpass",0,""],}

def clientthread(conn,client_list,ip): #each clientthread for each client. lasts until client logs out
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
  print(user + " is now online on ip: " + ip)
  #logged in
  while True:
  
    data = conn.recv(1024)
    if data[0:2] == "!q" :
      break
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
		
    elif data[0:9] == "!sendall ":
      #for member in client_list:
       # member.sendall(reply[9:])
		continue
    else:
      #conn.sendall(reply)
		continue

  conn.close()
  user_list[user][1] = 0
  user_list[user][2] = ''
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

client_list =[]
#send message back to client
while 1:
  conn, addr = s.accept() #conn is the socket object and addr is ip:port
  print("Connected with " + addr[0] + ":" + str(addr[1]))
  
  client_list.append(conn)
  
  start_new_thread(clientthread, (conn,client_list,addr[0]))

s.close()

