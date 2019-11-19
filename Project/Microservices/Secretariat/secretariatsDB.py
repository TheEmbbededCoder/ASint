import secretariats
import pickle

class secretariatsDB:
	def __init__(self, name):
		self.name = name
		try:
			f = open('secretariatsDB'+name, 'rb')
			self.sDB = pickle.load(f)
			f.close()
		except IOError:
			self.sDB = {}
	def addSecretariat(self, Location, Name, Description, OpeningHours):
		self.sDB[Name] = secretariats.secretariats(Location, Name, Description, OpeningHours)
		f = open('secretariatsDB'+self.name, 'wb')
		pickle.dump(self.sDB, f)
		f.close()
	
	def listAllSecretariats(self):
		return list(self.sDB.values())
	
	def showSecretariat(self, Name):
		try:
			return self.sDB[Name]
		except:
			pass


	def getLocation(self, Name):
		try:
			secr = self.sDB[Name]
			return secr.Location
		except:
			pass

	def getDescription(self, Name):
		try:
			secr = self.sDB[Name]
			return secr.description
		except:
			pass

	def getOpenhours(self, Name):
		try:
			secr = self.sDB[Name]
			return secr.openhours
		except:
			pass


