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

    # Create Loans
    @staticmethod
    def createLoan(member: User, book: Book, borrowDate, returnDate, renewCount):
        # Loan for book should not already exist
        if not Loan.getUserLoanByBook(member.email, book.title) and book.available:
            loan = Loan(
                member = member,
                book = book,
                borrowDate = borrowDate, # DUE DATE IS EXTRAPOLATED FRO THIS
                # returnDate = returnDate, # THIS IS WHEN YOU RETURNED IT, OPTIONAL FIELD
                renewCount = renewCount
            ).save()
            # Update book avail. if successful
            book.borrowBook()

            return loan

    # Retrieve Loans
    @staticmethod
    def getLoansByUser(email):
        return Loan.objects(member=User.getUser(email))
    
    @staticmethod
    def getUserLoanByBook(email, title):
        return Loan.objects(member=User.getUser(email), book=Book.getBook(title)).first()

    # Update Loans
    def renewLoan(self, new_date):
        self.borrowDate = new_date
        self.renewCount += 1
        self.save()

    def returnLoan(self, new_date):
        self.returnDate = new_date
        self.save()
        self.book.returnBook()
    
    # Delete Loans
    def deleteLoan(self):
        # TODO Implement check to check if book is returned.
        self.delete()
