from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import bookDB
import book

app = Flask(__name__)
db = bookDB.bookDB("mylib")
for bk in db.listAllBooks():
	print(bk)

@app.route('/')
def hello_world():
	count = len(db.listAllBooks())
	return render_template("mainPage.html", count_books=count)

@app.route('/addBooksForm')
def add_Book_Form():
	return render_template("addBookTemplate.html")

@app.route('/addBook', methods=['POST', 'GET'])
def add_Book():
	if request.method == "GET":
		Author = request.args['Author']
		Title = request.args['Title']
		Year = request.args['Year']
		db.addBook(Author, Title, Year)
		return redirect(url_for("hello_world"))
	else:
		db.addBook(request.form["Author"], request.form["Title"], request.form["Year"])
		return redirect(url_for("hello_world"))
	return render_template("addBookTemplate.html")

@app.route('/showBookForm')
def show_Book_Form():
	return render_template("showBookTemplate.html")

@app.route('/showBook', methods=['POST', 'GET'])
def show_Book():
	if request.method == "GET":
		id_b = request.args['id']
		book = db.showBook(int(id_b))
		print(book)
		return render_template("showBookTemplate.html", id=book.id, author=book.author, title=book.title, year=book.year)
	else:
		print(request.form["id"])
		book = db.showBook(int(request.form["id"]))
		print(book)
		if book is not None:
			return render_template("showBookTemplate.html", id=book.id, author=book.author, title=book.title, year=book.year)
		else:
			return render_template("showBookTemplate.html")
	return render_template("showBookTemplate.html")

@app.route('/listAllBooks')
def listAllBooks():
	list_bk = db.listAllBooks()
	print(list_bk)
	return render_template("listAllBooksTemplate.html", number_of_books = len(list_bk), books = list_bk)

@app.route('/listBooksYearForm')
def show_Book_Year_Form():
	return render_template("showBookByYearTemplate.html")

@app.route('/listBooksYear', methods=['POST', 'GET'])
def show_Book_Year():
	if request.method == "GET":
		year = int(request.args['year'])
		print(year)
		book_list = db.listBooksYear(year)
		print(book_list)
		return render_template("showBookByYearTemplate.html", year= year, number_of_books = len(book_list), books = book_list)
	else:
		year = int(request.form["year"])
		print(year)
		book_list = db.listBooksYear(year)
		print(book_list)
		if book_list is not None:
			return render_template("showBookByYearTemplate.html", year= year, number_of_books = len(book_list), books = book_list)
		else:
			return render_template("showBookByYearTemplate.html")
	return render_template("showBookByYearTemplate.html")

@app.route('/listBooksAuthorForm')
def show_Book_Author_Form():
	return render_template("showBookByAuthorTemplate.html")

@app.route('/listBooksAuthor', methods=['POST', 'GET'])
def show_Book_Author():
	if request.method == "GET":
		author = str(request.args['author'])
		print(author)
		book_list = db.listBooksAuthor(author)
		print(book_list)
		return render_template("showBookByAuthorTemplate.html", author = author, number_of_books = len(book_list), books = book_list)
	else:
		author = str(request.form["author"])
		print(author)
		book_list = db.listBooksAuthor(author)
		print(book_list)
		if book_list is not None:
			return render_template("showBookByAuthorTemplate.html", author = author, number_of_books = len(book_list), books = book_list)
		else:
			return render_template("showBookByAuthorTemplate.html")
	return render_template("showBookByAuthorTemplate.html")


########## REST API ###########

@app.route('/API/books')
def API_books():
	list_bk = db.listAllBooks()
	list_ID = []
	for bk in list_bk:
		list_ID.append(bk.id)
	return jsonify(list_ID)

@app.route('/API/books/<id>')
def API_book_ID(id):
	book = db.showBook(int(id))
	book_dict = {
		'id' : book.id,
		'name' : book.title,
		'year' : book.year,
		'author' : book.author
	}
	message = {
        'status': 200,
        'message': 'OK',
        'book': book_dict
    }
	print(message)
	return jsonify(message)

@app.route('/API/authors')
def API_authors():
	list_bk = db.listAllBooks()
	list_authors = []
	for bk in list_bk:
		if bk.author not in list_authors:
			list_authors.append(bk.author)
	return jsonify(list_authors)

@app.route('/API/authors/<author>')
def API_authors_books(author):
	book_list = db.listBooksAuthor(author)
	books = []
	for bk in book_list:
		book_dict = {
			'id' : bk.id,
			'name' : bk.title,
			'year' : bk.year,
			'author' : bk.author
		}
		books.append(book_dict)

	return jsonify(books)
	

if __name__ == '__main__':
	app.run()
