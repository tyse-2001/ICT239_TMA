from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.books import Book
from models.forms import BookForm


books = Blueprint("books", __name__)

# Helper Functions
def getCategories():
    categories = []
    for book in Book.getAllBooks():
        if book["category"] not in categories:
            categories.append(book["category"])
    return categories


def getBooks(category: str) -> list:
    if category == "All":
        return Book.getAllBooks()
    else:
        books = []
        for book in Book.getAllBooks():
            if book["category"] == category:
                books.append(book)

        return books


def getBook(title: str) -> dict:
    for i in Book.getAllBooks():
        if i["title"] == title:
            return i
    
    return None


@books.route("/bookTitles", methods=['GET', 'POST'])
def book_titles():
    books = Book.getAllBooks()
    if request.method == "GET":
        return render_template("book_titles.html", books = books, categories = getCategories(), panel="Book Titles")
    else:
        return render_template(
            "book_titles.html",
            books = getBooks(request.form.get('category').title()), 
            categories = getCategories(), panel="Book Titles"
        )


@books.route("/bookTitles/<title>")
def book_details(title):
    return render_template("book_details.html", book=getBook(title), panel="Book Details")


@books.route("/newBook", methods = ['GET', 'POST'])
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        existing_book = Book.getBook(title=form.title.data)
        if not existing_book:
            authors = []

            if form.author_1.data:
                if form.is_illustrator_1.data:
                    authors.append(f"{form.author_1.data} (Illustrator)")
                else:
                    authors.append(form.author_1.data)
            
            if form.author_2.data:
                if form.is_illustrator_2.data:
                    authors.append(f"{form.author_2.data} (Illustrator)")
                else:
                    authors.append(form.author_2.data)
            
            if form.author_3.data:
                if form.is_illustrator_3.data:
                    authors.append(f"{form.author_3.data} (Illustrator)")
                else:
                    authors.append(form.author_3.data)
            
            if form.author_4.data:
                if form.is_illustrator_4.data:
                    authors.append(f"{form.author_4.data} (Illustrator)")
                else:
                    authors.append(form.author_4.data)
            
            if form.author_5.data:
                if form.is_illustrator_5.data:
                    authors.append(f"{form.author_5.data} (Illustrator)")
                else:
                    authors.append(form.author_5.data)

            book = Book.createBook(
                genres=form.genres.data,
                title=form.title.data,
                category=form.category.data,
                url=form.url.data,
                description=form.description.data.splitlines(),
                authors=authors,
                pages=form.pages.data,
                available=form.copies.data,
                copies=form.copies.data
            )
            flash(f"{book.title} added")
            return redirect(url_for("books.new_book"))
        else:
            flash(f"{form.title.data} already exists")
            form.title.errors.append(f"{form.title.data} already exists")
            return render_template("new_book.html", form=form, panel="Add a book")


    return render_template("new_book.html", form=form, panel="Add a book")
