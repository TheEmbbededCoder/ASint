#!/usr/bin/env python

import Pyro4
import bookDB




#Pyro4.config.SERIALIZERS_ACCEPTED.add('serpent')

def main():

	daemon = Pyro4.Daemon(host="194.210.158.48")
	remoteLibrary = Pyro4.expose(bookDB.bookDB)
	#uri = daemon.register(remoteLibrary, 'FranciscoDB-123')
	uri = daemon.register(bookDB.bookDB, 'FranciscoDB-123')
	ns = Pyro4.locateNS(host="146.193.41.139", port=9090)
	print (uri)
	ns.register('FranciscoDB-123', uri)

	db = bookDB.bookDB("mylib")

	try:
			daemon.requestLoop()
	finally:
			daemon.shutdown(True)

if __name__=="__main__":
		main() 
