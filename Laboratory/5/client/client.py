#!/usr/bishn/env python

import Pyro4
import dbUI


#Pyro4.config.SERIALIZER = 'serpent'

def main():
		ns = Pyro4.locateNS(host="146.193.41.139", port=9090)
		print(ns.list())
		try:
			uri = ns.lookup('FranciscoDB-123')
		except Exception:
			print("Pyro traceback:")
			print("".join(Pyro4.util.getPyroTraceback()))
		
		
		db = Pyro4.Proxy(uri)

		
		ui = dbUI.dbUI(db)
		ui.menu()

if __name__=="__main__":
		main() 
