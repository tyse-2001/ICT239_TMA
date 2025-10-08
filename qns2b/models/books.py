from qns2b import db


class Book(db.Document):
    meta = {"collection": "book"}
    genres = db.ListField(db.StringField())
    title = db.StringField()
    category = db.StringField()
    url = db.StringField()
    description = db.ListField(db.StringField())
    authors = db.ListField(db.StringField())
    pages = db.IntField()
    available = db.IntField()
    copies = db.IntField()

    @staticmethod
    def getBook(title):
        return Book.objects(title=title).first()

    @staticmethod
    def getAllBooks():
        books = Book.objects()        
        return sorted(list(books), key=lambda d: d["title"])

    @staticmethod
    def createBook(genres, title, category, url, description, authors, pages,\
                   available, copies):
        return Book(
            genres = genres,
            title = title,
            category = category,
            url = url,
            description = description,
            authors = authors,
            pages = pages,
            available = available,
            copies = copies
        ).save()

    def borrowBook(self):
        if self.available:
            self.available -= 1
            self.save()

    def returnBook(self):
        if self.available < self.copies:
            self.available += 1
            self.save()

