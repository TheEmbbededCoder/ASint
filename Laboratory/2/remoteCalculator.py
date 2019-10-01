import socket


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 12343
s.connect((host, port))
while 1:
	msg = input()
	byt = msg.encode()
	s.send(byt)
	if msg == 'exit':
		break
	elif msg == 'pop':
		result = s.recv(1024)
		print("Result: ", result.decode())
s.close 
