from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email

class ContactForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Email()])
    email = StringField('email',validators=[DataRequired()])
    number = StringField('number',validators=[DataRequired()])
    message = TextAreaField('message',validators=[DataRequired()])
    submit = SubmitField("Contact Us")
