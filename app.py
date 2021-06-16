from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_talisman import Talisman
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()
#importing database
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.config['MONGO_URI'] = str(os.getenv('MONGO_URI'))
talisman = Talisman(
    app,
    content_security_policy={
        'default-src': SELF,
        'img-src': '*',
        'script-src': [
            SELF,
            'some.cdn.com',
        ],
        'style-src': [
            SELF,
            'another.cdn.com',
        ],
    },
    content_security_policy_nonce_in=['script-src'],
    feature_policy={
        'geolocation': '\'none\'',
    }
)
mongo = PyMongo(app)
# Collections (tables)
taskMaster = mongo.db.taskmaster
freedomWall = mongo.db.blog_posts

dateToday = datetime.utcnow()

#The routing stuff

#homepage
@app.route('/')
def index():
    return render_template('index.html')

#Blog App
@app.route('/blog_posts', methods=['GET', 'POST'])
def posts():
    all_posts = freedomWall.find()
    if request.method == 'POST':
        post_title = request.form.get('title')
        post_content = request.form.get('content')
        post_author = request.form.get('author')
        freedomWall.insert_one({'title':post_title, 'content': post_content, 'author': post_author, 'datePosted': dateToday})
        return redirect('/blog_posts')
    else:
        return render_template('posts.html', posts=all_posts)

@app.route('/blog_post_delete/<oid>')
def blog_post_delete(oid):
    freedomWall.delete_one({'_id': ObjectId(oid)})
    return redirect(url_for('posts'))

@app.route('/blog_edit/<oid>', methods= ['GET', 'POST'])
def blog_edit(oid):
    post = freedomWall.find_one_or_404({'_id': ObjectId(oid)})
    if request.method == 'POST':
        post_title = request.form.get('title')
        post_content = request.form.get('content')
        post_author = request.form.get('author')
        freedomWall.update_one({'_id': ObjectId(oid)},{'$set':{'title':post_title, 'content': post_content, 'author': post_author, 'dateEdited': dateToday}})
        return redirect('/blog_posts')
    else:
        return render_template('blog_edit.html', post=post)

#To-do app
@app.route('/add_task', methods=['POST'])
def task():
    new_task = request.form.get('content')
    taskMaster.insert_one({'text' : new_task , 'date' : dateToday})
    return redirect('/task')

@app.route('/task')
def task_page():
    tasks = taskMaster.find()
    return render_template('task.html', tasks=tasks)

@app.route('/task_delete/<oid>')
def task_delete(oid):
    taskMaster.delete_one({'_id': ObjectId(oid)})
    return redirect(url_for('task_page'))

@app.route('/task_update/<oid>', methods = ['GET', 'POST'])
def task_update(oid):
    task = taskMaster.find_one_or_404({'_id': ObjectId(oid)})
    if request.method == 'POST':
        update_task = request.form.get('content')
        taskMaster.update_one({'_id': ObjectId(oid)},{'$set':{'text': update_task}})
        return redirect(url_for('task_page'))
    else:
        return render_template('task_update.html', task = task)

if __name__ == "__main__":
    app.run(debug=True) #if there are errors, it will show on the page