# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from capstone import db
from capstone.models import User, BlogPost
from capstone.users.forms import RegistrationForm,LoginForm

users = Blueprint('users',__name__)

# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)



# login
@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))



@users.route("/account")
@login_required
def account():
    email=current_user.email
    user = User.query.filter_by(email=email).first_or_404()
    print("******************")
    # print(user.posts[0].date)
    # print(user.posts[0].title)
    # print(user.posts[0].file)

    # blog_posts = BlogPost.query.filter_by(user_id=user.id).order_by(BlogPost.date.desc())
    blog_posts=user.posts
    print(type(blog_posts))
    print("****************")
    print(blog_posts)
    return render_template('user_blog_posts.html',blog_posts=blog_posts)





