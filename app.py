from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

#importing database
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#tells the app where the database is located
db = SQLAlchemy(app) #initialize database

#Tables/Entities
class toDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    dateCreated = db.Column(db.DateTime, default =datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Anonymous User')
    datePosted = db.Column(db.DateTime, nullable = False , default =datetime.utcnow)

    def __repr__(self):
        return 'Blog post' + str(self.id)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']#connects to text area
        new_task = toDo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue creating this task'

    else:
        tasks = toDo.query.order_by(toDo.dateCreated).all()
        return render_template('index.html', tasks=tasks)#returns homepage

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
        return redirect('/')
    except:
        return 'There was an issue deleting this task'

@app.route('/task_update/<int:id>', methods = ['GET', 'POST'])
def task_update(id):
    task = toDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating this task'
    else:
        return render_template('task_update.html', task=task)

#Blog Posts
@app.route('/blog_posts', methods=['GET', 'POST'])
def posts():
    
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog_posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.datePosted).all()
        return render_template('posts.html', posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True) #if there are errors, it will show on the page
