from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

#importing database
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#tells the app where the database is located
db = SQLAlchemy(app) #initialize database

class toDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    dateCreated = db.Column(db.DateTime, default =datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


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

@app.route('/delete/<int:id>')
def delete(id):
    taskToDelete = toDo.query.get_or_404(id)
    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting this task'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = toDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating this task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True) #if there are errors, it will show on the page
