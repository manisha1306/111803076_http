#!/usr/bin/python

#Importing Necessary Modules

from socket import *
import  datetime
import sys
import os
import binascii
import threading
import logging
import time
import config
import random

#POST Handling Function to  Submit form
#Takes filename as input and reads the  file and sends it back

def post_file_handling(name,post2):
		f= open(name,"w+")
		if(f):
			print("102 PROCESSING\n")
		f.write(post2)
		f.close()		

#Authentication Function to Check User Credentials Before Deleting a FILE
#Takes USER_ID and PASSWORD as input compares it and Grants DELETE request

def authentication_del(connectionSocket):
	auth_msg = "401 UNAUTHORISED:\n"
	connectionSocket.send(auth_msg)
	user_msg = "Enter Your USER ID: "
	connectionSocket.send(user_msg)
	user_id = connectionSocket.recv(1024).decode()
	split1 = user_id.split()
	print(split1[0])					
	pass_msg = "Enter Your PASSWORD: "
	connectionSocket.send(pass_msg)
	password = connectionSocket.recv(1024).decode()
	split2 = password.split()
	print(split2[0])
	logging.basicConfig(filename="example.log", level=logging.INFO)
	logging.info('{}  {} --> Authenticating The USER_ID and PASSWORD'.format((date),(time)))
	if split1[0] == "admin" and split2[0] == "1234":
		logging.basicConfig(filename="example.log", level=logging.INFO)
		logging.info('{}  {} --> Authentication SUCCESSFUL'.format((date),(time)))
		return 1
	else:
		message ="401 UNAUTHORISED\n"
		connectionSocket.sendall(message.encode())
		connectionSocket.close()
		
#Function to Delete a FILE 
		
def delete_file(delete_name):
	delete = 'rm {}'.format(delete_name)
	os.system(delete)
	logging.basicConfig(filename="example.log", level=logging.INFO)
	logging.info('{}  {} --> DELETING FILE {}'.format((date),(time),(delete_name)))
	return 1
		
#Function to UPDATE a file (if it exists) during a PUT request	
		
def update_file_put(name_put,content):
	root = "/home/shri/Music/TY/CN/Project/{}".format(name_put)
	if os.path.isfile(root):
		f = open(root,"a")
		f.write(content)
		return 0

#Creating a Socket, Binding it
#Listening on the Socket

def socket_define():
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	time = now.strftime("%H:%M:%S")
	serverPort = (config.port)or(sys.argv[1])
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',serverPort))
	serverSocket.listen(1)
	print('The server is ready to receive')
	while(1):
		connectionSocket , addr = serverSocket.accept()
		print('new request received from'); 
		print(addr);
		logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
		logging.info('{}  {} --> Client {} has been connected '.format((date),(time),(addr)))	
		server_active(connectionSocket,addr)
	
#Activating the Server 

def server_active(connectionSocket,addr):
	print('connectionSocket is'); print(connectionSocket);
	sent = connectionSocket.recv(1024).decode()
	print("100 CONTINUE...")
	request_handling(sent, connectionSocket, addr)

#Function to Handle  Requests

def request_handling(sent, connectionSocket, addr):
	print("102 PROCESSING>>>")
	print(sent)
	words = sent.split()
#	op=[]
#	for i in  range(0,20):
#		op.append(words[i])
#	print(op)
	print(words)
	input_file=words[1].split('/')
	print(input_file)
	filename=input_file[1]
	print(filename)
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	time = now.strftime("%H:%M:%S")
	if(words[0] == "GET"):
		handle_get_request(date, time, connectionSocket, addr,filename)
	elif(words[0] == "HEAD"):
		print("1")
		handle_head_request(date, time, connectionSocket, addr,filename)
	elif(words[0] == "PUT"):
		handle_put_request(date, time, connectionSocket, addr,words)
	elif(words[0] == "DELETE"):
		handle_delete_request(date, time, connectionSocket, addr,words)
	else:
		print("404 BAD REQUEST\n")

#Function to Handle GET request

def handle_get_request(date, time, connectionSocket, addr,filename):
	try:
		f = open(filename, 'r')	
		if(f):
			logging.basicConfig(filename="example.log", level=logging.DEBUG)
			logging.info('{}  {} --> Client {} has requested for {}'.format((date),(time),(addr),(filename)))	
			response = f.read()
			if(response == ""):
				cookie_id=random.randint(1,10000)
				print("204 NO CONTENT\n")
				string = "\nHTTP/1.1 200 OK\n"
				string += "DATE AND TIME: {} {}\n".format(date,time)
				string += "SERVER: SHRIJEET's Server\n"
				string += "Set-Cookie: Http_cookie="+str(cookie_id)
				string += "Content type: image/jpeg; Charset=iso-8859-1\r\n"
				string += "Content Length : {}\n\n".format(len(response))
				filename = "access.log"
				logging.basicConfig(filename="example.log", level=logging.INFO)
				logging.info('{}  {} --> GET Request Successful by {} for {}'.format((date),(time),(addr),(filename)))		
				output = string + response
				connectionSocket.sendall(output.encode())	
				connectionSocket.close()
			elif(response):
				cookie_id=random.randint(1,10000)
				string = "\nHTTP/1.1 200 OK\n"
				string += "DATE AND TIME: {} {}\n".format(date,time)
				string += "SERVER: SHRIJEET's Server\n"
				string += "Set-Cookie: Http_cookie="+str(cookie_id)
				string += "Content type: image/png\r\n"
				string += "Content Length : {}\n\n".format(len(response))
				filename = "access.log"
				logging.basicConfig(filename="example.log", level=logging.INFO)
				logging.info('{}  {} --> GET Request Successful by {} for {} '.format((date),(time),(addr),(filename)))		
				output = string + response
				connectionSocket.sendall(output.encode())	
				connectionSocket.close()
			else:
				print("\n 422 UNPROCESSABLE ENTITY")
				logging.basicConfig(filename="example.log", level=logging.ERROR)
				logging.error('{}  {} --> GET Request NOT Successful for {} Index.html'.format((date),(time),(addr)))		
				connectionSocket.close()
		
	except:
		message="404 NOT FOUND\n"
		logging.basicConfig(filename="example.log", level=logging.DEBUG)
		logging.info('{}  {} --> Client {} has requested for {} BUT it DOES NOT EXIST'.format((date),(time),(addr),(filename)))
		connectionSocket.sendall(message.encode())	
		connectionSocket.close()
		
	
#Function to Handle HEAD Request
	
def handle_head_request(date, time, connectionSocket, addr,filename):
	logging.basicConfig(filename="example.log", level=logging.INFO)
	logging.info('{}  {} --> Client {} has requested for HEAD REQUEST {}'.format((date),(time),(addr),(filename)))
	last_modified=os.system('date -r index.html +%m-%d-%Y')
	f = open(filename)
	response = f.read()
	if(response):
		string   ="HTTP/1.1 200 OK\r\n"
		string +="Date: {} {}\r\n".format(date,time)
		string +="Server: Shrijeet's Server\r\n"
		string +="Last-Modified: {}\r\n".format(last_modified)
		string +="ETag:33a64df551425fcc55e4d42a148795d9f25f89d4\r\n"
		string +="Accept-Ranges: bytes\r\n"
		string +="Content-Length:{}\r\n\n".format(len(response))
		string +="Content-Type: text/html\r\n"
		string +="Connection: close\r\n"
		logging.basicConfig(filename="example.log", level=logging.INFO)
		logging.info('{}  {} --> HEAD Request Successful by {} for {} '.format((date),(time),(addr),(filename)))		
		connectionSocket.sendall(string.encode())	
		connectionSocket.close()
	else:
		message=" 422 UNPROCESSABLE ENTITY"
		logging.basicConfig(filename="example.log", level=logging.ERROR)
		logging.error('{}  {} --> HEAD Request NOT Successful '.format((date),(time)))		
		connectionSocket.sendall(message.encode())	
	
#Function to handle PUT  Request
	
def handle_put_request(date, time, connectionSocket, addr,words):
#	print(name_put)
#	name=[]
#	name=name_put
#	for i in len(name):
#	name_file = str(name[i])
	name_put=words[1]
	name = name_put.split('/')
	host=connectionSocket.recv(1024).decode()
	file_type=connectionSocket.recv(1024).decode()
	content=connectionSocket.recv(1024).decode()
	update = update_file_put(name[1],content)
	logging.basicConfig(filename="example.log", level=logging.INFO)
	logging.info('{}  {} --> Client {} has requested for PUT REQUEST in file {}'.format((date),(time),(addr),(name[1])))
	if(update == 0):
		pass
	else:
		f = open(name[1],"w")
		if(f):
			logging.basicConfig(filename="example.log", level=logging.INFO)
			logging.info('{} {} -->Client {} has requested to make  changes in file {}'.format((date),(time),(addr),(name[1])))		
			f.write(content)
			f.close()
		else:
			print("\n 422 UNPROCESSABLE ENTITY")
			logging.basicConfig(filename="example.log", level=logging.DEBUG)
			logging.debug('{}  {} --> PUT Request NOT Successful for {} '.format((date),(time),(name[1])))		
	string ="HTTP/1.1 200 OK\n"	
	string +="Host:Localhost\n"
	string +="ServerName:Shrijeet's Server\n"
	connectionSocket.sendall(string.encode())
	logging.basicConfig(filename="example.log", level=logging.INFO)
	logging.info('{}  {} --> PUT Request Successful by {} for {} '.format((date),(time),(addr),(name[1])))			
	connectionSocket.close()
	
#Function to  Handle Delete Request
	
def handle_delete_request(date, time, connectionSocket, addr,words):
	name_del=words[1]
	name = name_del.split('/')
	logging.basicConfig(filename="example.log", level=logging.INFO)
	logging.info('{}  {} --> Client {} has requested for DELETE REQUEST for file {}'.format((date),(time),(addr),(name[1])))
	authenticate_val = authentication_del(connectionSocket)
	if(authenticate_val == 1):
		delete_name=name[1]
		del_file = delete_file(delete_name)
		if(del_file):
			string = "HTTP/1.1 200 OK \n"
			string += "DATE AND TIME: {} {}\n".format(date,time)			
			connectionSocket.send(string)				
		else:	
			string = "404 File Not Found"
			logging.basicConfig(filename="example.log", level=logging.INFO)
			logging.info('{}  {} --> Client\'s Requested File {} NOT Found '.format((date),(time),(name[1])))
			connectionSocket.send(string)
	else:
		string1="203 Non Authoritative Information\n"
		connectionSocket.send(string1)
	connectionSocket.close()
	
#Main

if __name__ == "__main__": 
	socket_define()

#Multithreading Of Requests	

thread = threading.Thread(target=handle_get_request, args=(date, time, connectionSocket, addr))
thread.start()

thread = threading.Thread(target=handle_head_request, args=(date, time, connectionSocket, addr))
thread.start()

thread = threading.Thread(target=handle_put_request, args=(date, time, connectionSocket, addr,words))
thread.start()

thread = threading.Thread(target=handle_delete_request, args=(date, time, connectionSocket, addr,words))
thread.start()				





