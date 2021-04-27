import socket
import threading
import re


class Connection():
	def __init__(self,conn):
		self.connection = conn
		

class Server():
	def __init__(self,host,inPort,outPort):
		self.host = host
		self.inPort = inPort
		self.outPort = outPort
		self.connections = []
		self.headers = {
			200 : "HTTP/1.0 200 OK\n\n",
			404 : "HTTP/1.0 404 Not Found\n\n",
			500 : "HTTP/1.0 500 Internal server error\n\n"
		}

	def readFile(self,file):
		path = "www"+file
		print("Reading from path: "+path)
		try:
			with open(path, 'r') as reader:
				return reader.read()
		except IOError:
			print("File not found.")
			return False

	def start(self,):
		print("Started.")
		while True:
			print("\nWaiting for connection...")
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.bind((self.host, self.inPort))
				s.listen()
				conn, addr = s.accept()

				with conn:
					print("Connected by: "+str(addr))
					data = conn.recv(1024)
					data = data.decode().split('\r\n')
					requester = addr[0]+":"+str(addr[1]) #Requester's ip and port in printable format.

					for d in data:
						if "GET" in d:
							#GET(.*[a-z])
							file = re.match("GET (.*?.(html|css|js|\s))",d)
							if file:
								filename = file[1]
								if filename == "/ ":
									filename= "/index.html"
								print(requester+" requested: "+filename)


								rfile = self.readFile(filename)
								if rfile != False:
									response = self.headers[200]+rfile
								else:
									response = self.headers[404]
								conn.sendall(response.encode())
							else:
								response = 'HTTP/1.0 404 Not Found\n\n'
								print("No idea what "+requester+" wants ¯\_(ツ)_/¯")


					
					
					conn.close()
					print("Connection closed for: "+requester)

				
	



if __name__ == '__main__':
	s = Server("127.0.0.1",3000,3001)
	s.start()

