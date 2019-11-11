"""
Created on Fri Oct 10 10:02:24 2014

@author: jnos
"""
import book
import pickle


class bookDB:
	def __init__(self, name):
		self.name = name
		try:
			f = open('bd_dump'+name, 'rb')
			self.bib = pickle.load(f)
			f.close()
		except IOError:
			self.bib = {}
	def addBook(self, author, title, year):
		print("1")
		b_id = len(self.bib)
		print("2")
		self.bib[b_id] = book.book(author, title, year, b_id)
		print("3")
		f = open('bd_dump'+self.name, 'wb')
		print("4")
		pickle.dump(self.bib, f)
		print("5")
		f.close()
		print("6")
		return b_id
	def getBook(self, b_id):
		book = {
			'author' : self.bib[b_id].author,
			'title' : self.bib[b_id].title,
			'year' : self.bib[b_id].year,
			'id' : self.bib[b_id].id,
		}
		return book

	def listAllBooks(self):
		books = []
		for key, value in self.bib.values():
			books.append[value.id]
		return books

	def listBooksAuthor(self, authorName):
		ret_value = []
		for b in self.bib.values():
			if b.author == authorName:
				ret_value.append(b.id)
		return ret_value
	def listBooksYear(self, year):
		ret_value = []
		for b in self.bib.values():
			if b.year == year:
				ret_value.append(b.id)
		return ret_value


