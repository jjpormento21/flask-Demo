from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_pymongo import PyMongo
#importing database
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['MONGO_URI'] = 'mongodb+srv://admin:HnI37MkYad9M9PQp@cluster0.qg0ok.mongodb.net/theWebsite?retryWrites=true&w=majority'
mongo = PyMongo(app)
#tells the app where the database is located
db = SQLAlchemy(app) #initialize database
taskMaster = mongo.db.toDo

dateToday = datetime.utcnow()

idNum = 0

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    datePosted = db.Column(db.DateTime, nullable = False , default = datetime.utcnow)
    dateEdited = db.Column(db.String(30), nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return 'Blog post' + str(self.id)

#The routing stuff

#homepage
@app.route('/')
def index():
    return render_template('index.html')

#Blog Posts
@app.route('/blog_posts', methods=['GET', 'POST'])
def posts():
    #it is latest by default
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog_posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.datePosted.desc()).all()
        return render_template('posts.html', posts=all_posts)

#To-do app
@app.route('/add_task', methods=['POST'])
def task():
    global idNum
    new_task = request.form.get('content')
    idNum+=1
    taskMaster.insert_one({'text' : new_task , 'date' : dateToday, 'number' : idNum})
    return redirect('/task')

@app.route('/task')
def task_page():
    tasks = taskMaster.find()
    return render_template('task.html', tasks=tasks)

#Deleting Stuff
@app.route('/blog_post_delete/<int:id>')
def blog_post_delete(id):
    itemToDelete = BlogPost.query.get_or_404(id)
    try:
        db.session.delete(itemToDelete)
        db.session.commit()
        return redirect('/blog_posts')
    except:
        return 'There was an issue deleting this task'

@app.route('/task_delete/<int:id>')
def task_delete(id):
    itemToDelete = toDo.query.get_or_404(id)
    try:
        db.session.delete(itemToDelete)
        db.session.commit()
        return redirect('/task')
    except:
        return 'There was an issue deleting this task'

#Updating Stuff
@app.route('/blog_edit/<int:id>', methods= ['GET', 'POST'])
def blog_edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        post.dateEdited = request.form['dateEdited']
        db.session.commit()
        return redirect('/blog_posts')
    else:
        return render_template('blog_edit.html', post=post)

@app.route('/task_update/<int:id>', methods = ['GET', 'POST'])
def task_update(id):
    task = toDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/task')
        except:
            return 'There was an issue updating this task'
    else:
        return render_template('task_update.html', task=task)

#Filters
@app.route('/blog_posts_old', methods=['GET', 'POST'])
def posts_oldest():
    
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog_posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.datePosted).all()
        return render_template('posts.html', posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True) #if there are errors, it will show on the page