from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user
from models.loans import Loan


loans = Blueprint("loans", __name__)


# TODO Finish implementation
@loans.route("/newLoan",  methods = ['POST'])
def new_loan():
    if current_user.is_authenticated:
        pass
    else:
        flash("Please login or register first to get an account", "error")
        return redirect(url_for('auth.login'))
