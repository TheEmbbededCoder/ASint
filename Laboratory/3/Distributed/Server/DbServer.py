from bookDB import bookDB
import Pyro4

@Pyro4.expose
class dbUI(bookDB):
    def __init__(self):
        super().__init__()
    
    def addBook(self, author, title, year, bookid):
        self.NEW(author, title, year, bookid)

    def findBook(self, id):
        return self.SHOW(id)

    def listAuthors(self):
        return self.AUTHORS()

    def findByAuthor(self, author):
        return self.SEARCH_AUTH(author)
    
    def findByYear(self, year):
        return self.SEARCH_YEAR(year)


def main():
    daemon = Pyro4.Daemon()                # make a Pyro daemon
    uri = daemon.register(dbUI)   # register the greeting maker as a Pyro object
  
    print("Ready: "+str(uri))
    daemon.requestLoop()                   # start the event loop of the server to wait for calls


    
            

if __name__ == "__main__":
    main()
