from flask import Blueprint, render_template, request
from models.books import Book


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
