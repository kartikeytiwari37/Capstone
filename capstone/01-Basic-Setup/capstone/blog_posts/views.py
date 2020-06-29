# blog_posts/views.py
import secrets
import os
from flask import render_template,url_for,flash,request,redirect,Blueprint,send_file
from flask_login import current_user,login_required
from capstone import db
from capstone.models import BlogPost
from capstone.models import BlogPost
from capstone.blog_posts.forms import BlogPostForm
from flask import current_app
blog_posts = Blueprint('blog_posts',__name__)
from capstone.aqgFunction import AutomaticQuestionGenerator
# Upload_folder=os.path.join(current_app.root_path,'static/files')


def generate(filename):
    # Create AQG object
    aqg = AutomaticQuestionGenerator()

    #inputTextPath =r"C:\Users\hp\Downloads\Automatic-Question-Generator-master\AutomaticQuestionGenerator/DB/db.txt"
    inputTextPath=filename
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    #readFile = open(inputTextPath, 'r+', encoding="utf8", errors = 'ignore')

    inputText = readFile.read()
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''

    questionList = aqg.aqgParse(inputText)
    aqg.display(questionList)
    print("**********************")
    print(aqg.filename)
    print("**********************")
    

    #aqg.DisNormal(questionList)

    return aqg.filename+r".txt"
def save_file(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(current_app.root_path, 'static/files', audio_fn)

    
    form_file.save(audio_path)

    return audio_fn


# CREATE
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        file = save_file(form.file.data)
        filename=os.path.join(current_app.root_path, 'static/files', file)
        print("000000000000000000000000")
        print(filename)
        print("000000000000000000000000")
        output=generate(filename)
        blog_post = BlogPost(title=form.title.data,user_id=current_user.id,file=output)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('users.account'))

    return render_template('create_post.html',form=form)




# BLOG POST (VIEW)
# @blog_posts.route('/<int:blog_post_id>')
# def blog_post(blog_post_id):
#     blog_post = BlogPost.query.get_or_404(blog_post_id)
#     return render_template('blog_post.html',title=blog_post.title,
#                             date=blog_post.date,post=blog_post
#     )



# # UPDATE
# @blog_post.route('/<int:blog_post_id/update',methods=['GET','POST'])
# @login_required
# def update(blog_post_id):
#     blog_post = BlogPost.query.get_or_404(blog_post_id)

#     if blog_post.author != current_user:
#         abort(403)

#     form = BlogPostForm()


#     if form.validate_on_submit():

#         blog_post.title = form.title.data
#         blog_post.text = form.text.data
#         db.session.commit()
#         flash('Blog Post Updated')
#         return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))

#     elif request.method = 'GET':
#         form.title.data = blog_post.title
#         form.text.data = blog_post.text

#     return render_template('create_post.html',title='Updating',form=form)


# DELETE
@blog_posts.route('/account/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('users.account'))


@blog_posts.route('/download/<filename>')
@login_required
def download(filename):
    file_path = os.path.join(current_app.root_path, 'static/files', filename)
    return send_file(file_path, as_attachment=True, attachment_filename='')