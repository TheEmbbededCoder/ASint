import Pyro4
from book import Book

name = input("URI: ").strip()
print(name)
dbUI = Pyro4.Proxy(name)    # use name server object lookup uri shortcut
try:
    while True:
        print("Write intended action: [NEW, SHOW. AUTHORS, SEARCH_AUTH, SEARCH_YEAR]")
        command = input()
        if command == "NEW":
            print("<author> <title> <year> <bookid>")
            newbook = input()
            newbook = newbook.split()
            dbUI.addBook(newbook[0], newbook[1], newbook[2], newbook[3])
        elif command == "SHOW":
            bookid = input("book id: ")
            print(dbUI.findBook(bookid))
        elif command == "AUTHORS":
            print(dbUI.listAuthors())
        elif command == "SEARCH_AUTH":
            author = input("Author's name: ")
            print(dbUI.findByAuthor(author))
        elif command == "SEARCH_YEAR":
            year = input("Book's year: ")
            print(dbUI.findByYear(year))
        else:
            print("Command not recognized")
except:
    print("".join(Pyro4.util.getPyroTraceback()))