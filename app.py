# this are all the libraries that were used to create this python flask app
from flask import Flask, render_template, url_for, request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import time 


app = Flask(__name__) #this is creating the app and refering to itself 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #this is linking the app to the database in sqlite
db = SQLAlchemy(app) 

class Todo(db.Model): #creating a class using a Todo
    id = db.Column(db.Integer, primary_key=True) #creating a column using a primary key
    content = db.Column(db.String(200), nullable= False) #this is the content within the text box
    completed = db.Column(db.Integer, default=0) #this is a counter
    date_created = db.Column(db.DateTime, default= datetime.utcnow) #this is the date is was created 

    def __repr__(self): #function to return the id of the task
        return '<Task %r>' % self.id


@app.route('/', methods={'POST', 'GET'}) #this is a route to the main page and it contains 2 methods POST to send information and GET to get information 
def index():
    if request.method == 'POST': #this is a request method to see if there was anything to post
        task_content = request.form['content'] #if there is something to post then task_content will be set to the content inside the text bar

        new_task = Todo(content=task_content) #this is a new Todo that will set the content equal to the task_content

        try:
            db.session.add(new_task) #this will add the new task to the database
            db.session.commit()#commit to the database
            return redirect('/') #return to the mainpage
        
        except:
            return 'There was an issue adding your task' #if it did not succeed then this message will pop out 

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #if it is not a post then it will get all the tasks in the Todo 
        
        return render_template('index.html', tasks=tasks) #this will also render the main page and set all the tasks to tasks in order to display them 

@app.route('/delete/<int:id>') #this is another route for the delete
def delete(id): #this id a function and it uses the id to identify which task it is going to delete 
    task_to_delete = Todo.query.get_or_404(id) #this is setting the task_to_delete to the Todo id 

    try:
        db.session.delete(task_to_delete) #if it does match the id then it will delete it
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'#if it does not match then this message will be displayed


@app.route('/update/<int:id>', methods=['GET', 'POST'])#this is another route for the update and it will be using the 2 methods GET and POST 
def update(id): #the function will also be using id to identify which task will be updated
    task = Todo.query.get_or_404(id) #this is setting the task to the Todo id task
    if request.method == 'POST': #if the request.method is a post 
        task.content = request.form['content'] #then it will get the content inside the content and set it to task

        try:
            db.session.commit()#this will commit and return to the main page if it was successfull
            return redirect('/')
        except:
            return 'There was an issue updating your task'#if not then this message will be displayed
    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)