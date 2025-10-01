from datetime import date, timedelta
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
    def createLoan(member: User, book: Book, borrowDate, renewCount):
        latest_loan = Loan.getUserLoanByBook(member.email, book.title)
        
        # Past loans can exist, but must be returned first.
        if not latest_loan or latest_loan.returnDate and book.available:
            loan = Loan(
                member = member,
                book = book,
                borrowDate = borrowDate,
                renewCount = renewCount
            ).save()
            # Update book avail. if successful
            book.borrowBook()

            return loan

    @staticmethod
    def getLoansByUser(email):
        """ Get all loans by user in descending order """
        loans = Loan.objects(member=User.getUser(email))
        sorted_loans = loans.order_by("-borrowDate", "returnDate")
        return sorted_loans
    
    @staticmethod
    def getUserLoanByBook(email: str, title: str):
        """ Get the latest loan of specified book by user """
        loans = Loan.objects(member=User.getUser(email), book=Book.getBook(title))
        sorted_loans = loans.order_by("returnDate")
        return sorted_loans.first()

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
        if self.returnDate:
            self.delete()

    def get_dueDate(self) -> date:
        return self.borrowDate + timedelta(days=14)

    def is_overdue(self) -> bool:
        # Check if book is still loaned out
        if not self.returnDate:
            return date.today() > self.get_dueDate()
        return False
