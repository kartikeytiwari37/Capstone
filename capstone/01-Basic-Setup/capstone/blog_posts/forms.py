from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from capstone.models import User


class BlogPostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    file = FileField('Upload Text File', validators=[FileAllowed(['txt'])])
    submit1 = SubmitField("Submit")


class BlogPostForm2(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit2 = SubmitField('Submit')
