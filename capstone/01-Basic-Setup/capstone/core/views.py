from flask import render_template,url_for,flash,request,redirect,Blueprint
from capstone import db
from capstone.models import ContactPost
from capstone.core.forms import ContactForm
core = Blueprint('core',__name__)



@core.route('/',methods=['GET','POST'])
def index():
    form = ContactForm()
    contact=ContactPost.query.all()
    print(contact)
    form.name.data=""
    form.email.data=""
    form.number.data=""
    form.message.data=""

    if form.validate_on_submit():

        contactpost = ContactPost(name=form.name.data,
                            email=form.email.data,
                            number=form.number.data, message=form.message.data
                            )
        db.session.add(contactpost)
        db.session.commit()
        flash('Contact Success')
        return redirect(url_for('core.index'))

    return render_template('landing.html',form=form)
