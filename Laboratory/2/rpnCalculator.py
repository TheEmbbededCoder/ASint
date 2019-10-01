import socket

class rpnCalculator:

	def __init__(self):
		self.memory = []

	def pushValue(self, value):
		self.memory.append(value)

	def popValue(self):
		try:
			return self.memory.pop()
		except:
			print("Empty Stack")

	def add(self):
		try:
			a = self.memory.pop()
			b = self.memory.pop()
			self.memory.append(a+b)
		except:
			print("Empty Stack")

	def sub(self):
		try:
			a = self.memory.pop()
			b = self.memory.pop()
			self.memory.append(a-b)
		except:
			print("Empty Stack")

	def printStack(self):
		print(self.memory)

if __name__ == '__main__':

	calculator = rpnCalculator()

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host = socket.gethostname()
	port = 12343
	s.bind((host, port))
	s.listen(5)
	while True:
		c, addr = s.accept()
		print('Connection from', addr)

		while True:
			msg = c.recv(1024)
			print("Received: ", msg.decode())
			msg = msg.decode()
			msg = msg.split()

			if msg[0] == 'push':
				calculator.pushValue(float(msg[1]))
			elif msg[0] == 'pop':
				result = str(calculator.popValue())
				byt = result.encode()
				c.send(byt)
			elif msg[0] == 'add':
				calculator.add()
			elif msg[0] == 'sub':
				calculator.add()
			elif msg[0] == 'exit':
				break
			else:
				calculator.printStack()

		c.close()


	#	calculator.pushValue(1)
	#	calculator.pushValue(2)
	#	calculator.pushValue(3)
	#	calculator.pushValue(4)
	#	calculator.pushValue(5)
	#	print("Stack: ", calculator.printStack())
	#	print("Pop value: ", calculator.popValue())
	#	print("Stack: ", calculator.printStack())
	#	print("Add: ", calculator.add())
	#	print("Stack: ", calculator.printStack())
	#	print("Pop value: ", calculator.popValue())
	#	print("Stack: ", calculator.printStack())
	#	print("Sub: ", calculator.sub())
	#	print("Stack: ", calculator.printStack())
	#	print("Pop value: ", calculator.popValue())
	#	print("Stack: ", calculator.printStack())