from qns2b import db
from models.users import User
from models.books import Book


class Loan(db.Document):
    meta = {"collection": "loan"}
    member = db.ReferenceField(User)
    book = db.ReferenceField(Book)
    borrowDate = db.DateField()
    returnDate = db.DateField()
    renewCount = db.IntField()
