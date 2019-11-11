from bookDB import bookDB

class dbUI(bookDB):
    def __init__(self):
        super().__init__()
    
    def addBook(self, author, title, year, bookid):
        self.NEW(author, title, year, bookid)

    def findBook(self, id):
        return self.SHOW(id)

    def listAuthors(self):
        self.AUTHORS()

    def findByAuthor(self, author):
        self.SEARCH_AUTH(author)
    
    def findByYear(self, year):
        self.SEARCH_YEAR(year)


def main():
    dbui = dbUI()

    while True:
        print("Write intended action: [NEW, SHOW. AUTHORS, SEARCH_AUTH, SEARCH_YEAR]")
        command = input()
        if command == "NEW":
            print("<author> <title> <year> <bookid>")
            newbook = input()
            newbook = newbook.split()
            dbui.addBook(newbook[0], newbook[1], newbook[2], newbook[3])
        elif command == "SHOW":
            bookid = input("book id: ")
            print(dbui.findBook(bookid))
        elif command == "AUTHORS":
            dbui.listAuthors()
        elif command == "SEARCH_AUTH":
            author = input("Author's name: ")
            dbui.findByAuthor(author)
        elif command == "SEARCH_YEAR":
            year = input("Book's year: ")
            dbui.findByYear(year)
        else:
            print("Command not recognized")
            

if __name__ == "__main__":
    main()
