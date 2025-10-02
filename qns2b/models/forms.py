from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, \
    SelectField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import Email, InputRequired, URL


class RegForm(FlaskForm):
    email = StringField(
        "Email", 
        validators=[
            InputRequired(), 
            Email(message="Invalid email")
        ]
    )
    password = PasswordField("Password", validators=[InputRequired()])
    name = StringField("Name")


class BookForm(FlaskForm):
    genres = SelectMultipleField("Choose multiple Genres:", choices= [
        "Animals", "Business", "Comics", "Communication", "Dark Academia", 
        "Emotion", "Fantasy", "Fiction", "Friendship", "Graphic Novels", 
        "Grief", "Historical Fiction", "Indigenous", "Inspirational", "Magic",
        "Mental Health", "Nonfiction", "Personal Development", "Philosophy", 
        "Picture Books", "Poetry", "Productivity", "Psychology", "Romance",
        "School", "Self Help"
    ], validators=[InputRequired()])
    title = StringField("Title", validators=[InputRequired()])
    category = SelectField("Choose a category:", choices=[
        "Adult", "Teens", "Children"
    ], validators=[InputRequired()])
    url = StringField("URL for Cover", validators=[InputRequired(), URL()])
    description = TextAreaField("Description:", validators=[InputRequired()])
    author_1 = StringField("Author 1:", validators=[InputRequired()])
    is_illustrator_1 = BooleanField("Illustrator")
    author_2 = StringField("Author 2:")
    is_illustrator_2 = BooleanField("Illustrator")
    author_3 = StringField("Author 3:")
    is_illustrator_3 = BooleanField("Illustrator")
    author_4 = StringField("Author 4:")
    is_illustrator_4 = BooleanField("Illustrator")
    author_5 = StringField("Author 5:")
    is_illustrator_5 = BooleanField("Illustrator")
    pages = IntegerField("Number of pages:", validators=[InputRequired()])
    copies = IntegerField("Number of copies:", validators=[InputRequired()])