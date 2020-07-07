# blog_posts/views.py
access_key='AKIAQPXCCTPJBHJDWJES'
secret_access_key='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'
import boto3
import os
client=boto3.client('s3',aws_access_key_id=access_key,
                    aws_secret_access_key=secret_access_key)

s3 = boto3.resource(
    's3',
   
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key
)
upload_file_bucket='chinu-dummy-bucket'
import nltk
import secrets
import os
from flask import render_template,url_for,flash,request,redirect,Blueprint,send_file,Response
from flask_login import current_user,login_required
from capstone import db
from capstone.models import BlogPost
from capstone.models import BlogPost
from capstone.blog_posts.forms import BlogPostForm,BlogPostForm2
from flask import current_app
blog_posts = Blueprint('blog_posts',__name__)
from capstone.aqgFunction import AutomaticQuestionGenerator
# Upload_folder=os.path.join(current_app.root_path,'static/files')


def generate(filename):
    # Create AQG object
    aqg = AutomaticQuestionGenerator()

    #inputTextPath =r"C:\Users\hp\Downloads\Automatic-Question-Generator-master\AutomaticQuestionGenerator/DB/db.txt"
    file = client.get_object(Bucket='chinu-dummy-bucket', Key=filename)
    inputText=file['Body'].read().decode('utf-8')
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''

    questionList = aqg.aqgParse(inputText)
    aqg.display(questionList)
    print("**********************")
    print(aqg.filename)
    print("**********************")
    

    #aqg.DisNormal(questionList)

    return aqg.filename+r".txt"


def generate2(inputText):
    aqg = AutomaticQuestionGenerator()
    questionList = aqg.aqgParse(inputText)
    aqg.display(questionList)
    return aqg.filename+r".txt"

def save_file(form_file):
    print(form_file)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    upload_file_key = random_hex + f_ext

    client.upload_fileobj(form_file,upload_file_bucket,upload_file_key,ExtraArgs={
                "ACL": "public-read",
                "ContentType": form_file.content_type
            })

    return upload_file_key


# CREATE
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    form2=BlogPostForm2()

    if form.submit1.data and form.validate():
        file = save_file(form.file.data)
        output=generate(file)
        blog_post = BlogPost(title=form.title.data,user_id=current_user.id,file=output)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('users.account'))

    if form2.submit2.data and form2.validate():
        output=generate2(form2.text.data)
        blog_post = BlogPost(title=form2.title.data,user_id=current_user.id,file=output)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('users.account'))

    return render_template('create_post.html',form=form,form2=form2)




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
    file = client.get_object(Bucket='chinu-dummy-bucket', Key=filename)
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename=questions.txt"}
    )
   
@blog_posts.route('/view/<filename>')
@login_required
def view(filename):

    file = client.get_object(Bucket='chinu-dummy-bucket', Key=filename)
    inputText=file['Body'].read().decode('utf-8')
    sent_text = nltk.sent_tokenize(inputText)
    print(sent_text)
    return render_template('views.html',text=sent_text)