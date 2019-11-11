class Book:
    def __init__(self, author, title, year, bookid):
        self.author = author
        self.title = title
        self.year = int(year)
        self.id = bookid

    def __str__(self):
        return "Author: " + self.author + "\nTitle: " + self.title + "\nYear: " +  str(self.year) + "\n"

    def getID(self):
        return self.id

    def getAuthor(self):
        return self.author

    def getYear(self):
        return self.year