from flask import render_template, request

from qns2a import app
from books import all_books


def getCategories():
    categories = []
    for book in all_books:
        if book["category"] not in categories:
            categories.append(book["category"])
    return categories


def getBooks(category: str) -> list:
    if category == "All":
        return sorted(all_books, key=lambda d: d["title"])
    else:
        books = []
        for book in all_books:
            if book["category"] == category:
                books.append(book)

        sorted_books = sorted(books, key=lambda d: d["title"])
        return sorted_books


def getBook(title: str) -> dict:
    for i in all_books:
        if i["title"] == title:
            return i
    
    return None


@app.route("/bookTitles", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template(
            "book_titles.html", 
            books = getBooks("All"), 
            categories = getCategories(), 
            panel="Book Titles"
        )
    else:
        return render_template(
            "book_titles.html",
            books = getBooks(request.form.get('category').title()), 
            categories = getCategories(), panel="Book Titles"
        )


@app.route("/bookTitles/<title>")
def book_details(title):
    return render_template(
        "book_details.html", 
        book=getBook(title), 
        panel="Book Details"
    )
