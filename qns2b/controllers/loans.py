from datetime import date, timedelta
from random import randint
from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user
from models.loans import Loan
from models.books import Book


loans = Blueprint("loans", __name__)


def generate_date(x: date, add: bool) -> date: 
    new_date = date.today() + timedelta(days=1)
    while new_date > date.today():
        random_timedelta = timedelta(days=randint(10,20))
        if add:
            if x >= date.today() - timedelta(days=10):
                return date.today()
            new_date = x + random_timedelta
        else:
            new_date = x - random_timedelta
    
    return new_date


@loans.route("/newLoan/<title>")
def new_loan(title):
    if current_user.is_authenticated:
        book = Book.getBook(title)
        borrowDate = generate_date(date.today(), False)
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
    return_date = generate_date(loan.borrowDate, True)
    loan.returnLoan(return_date)
    flash(f"{loan.book.title} loan has been returned.", "success")
    return redirect(url_for('loans.display_loans'))


@loans.route("/loans/renewLoan/<title>")
def renew_loan(title):
    loan = Loan.getUserLoanByBook(current_user.email, title)
    new_borrowDate = generate_date(loan.borrowDate, True)
    loan.renewLoan(new_borrowDate)
    flash(f"{loan.book.title} loan has been renewed.", "success")
    return redirect(url_for('loans.display_loans'))


@loans.route("/loans/deleteLoan/<title>")
def delete_loan(title):
    loan = Loan.getUserLoanByBook(current_user.email, title)
    loan.deleteLoan()
    flash(f"{loan.book.title} loan has been deleted.", "success")
    return redirect(url_for('loans.display_loans'))
