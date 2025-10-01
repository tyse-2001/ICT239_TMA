from datetime import date, timedelta
from random import randint
from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user
from models.loans import Loan
from models.books import Book


loans = Blueprint("loans", __name__)


def generate_borrowDate() -> date:
    today = date.today()
    random_days = timedelta(days=randint(10, 20))
    return today - random_days


@loans.route("/newLoan/<title>")
def new_loan(title):
    if current_user.is_authenticated:
        book = Book.getBook(title)
        borrowDate = generate_borrowDate()
        loan = Loan.createLoan(current_user, book, borrowDate, 0)
        if loan:
            flash(f"{loan.book.title} has been loaned.", "success")
        else:
            flash("Error creating loan", "error")
        return redirect(url_for("home"))
    else:
        flash("Please login or register first to get an account", "error")
        return redirect(url_for('auth.login'))


@loans.route("/loans")
def display_loans():
    if current_user.is_authenticated:
        all_loans = Loan.getLoansByUser(current_user.email)
        return render_template("loans.html", all_loans= all_loans, panel="Current Loans")
    else:
        flash("Please login or register first to get an account", "error")
        return redirect(url_for('auth.login'))


@loans.route("/loans/returnLoan/<title>")
def return_loan(title):
    loan = Loan.getUserLoanByBook(current_user.email, title)
    loan.returnLoan()
    flash(f"{loan.book.title} has been returned.", "success")
    return redirect(url_for('loans.display_loans'))
