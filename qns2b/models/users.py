from flask_login import UserMixin

from qns2b import db


class User(UserMixin, db.Document):
    meta = {"collection": "users"}
    email = db.StringField()
    password = db.StringField()
    name = db.StringField()

    @staticmethod
    def getUser(email):
        return User.objects(email=email).first()
    
    @staticmethod 
    def createUser(email, name, password):
        user = User.getUser(email)
        if not user:
            user = User(email=email, name=name, password=password).save()
        return user  

    @staticmethod
    def getUserById(user_id):
        return User.objects(pk=user_id).first()
