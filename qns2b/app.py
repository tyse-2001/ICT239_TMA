from flask import redirect, url_for, request, render_template
from qns2b import app
from controllers.auth import auth
from controllers.books import books
from controllers.loans import loans
app.register_blueprint(auth)
app.register_blueprint(books)
app.register_blueprint(loans)


@app.template_filter("formatDate")
def formatDate(date):
    return date.strftime("%m %b %Y")


@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for('books.book_titles'))


@app.errorhandler(404)
def page_not_found(error):

    # Try to find the correct path if the capitalization is wrong
    path = request.path
    if path[1].isupper():
        return redirect(path[0] + path[1].lower() + path[2:])

    return render_template('error.html'), 404
