from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from capstone.models import User


class BlogPostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    file = FileField('Upload Text File', validators=[FileAllowed(['txt'])])
    submit = SubmitField("Submit")


