import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
s.connect((host, port))
msg = input()
byt = msg.encode()
s.send(byt)
s.close 
