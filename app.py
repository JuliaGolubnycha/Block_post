from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime

app = Flask(__name__) #This line must be in every similar app
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3' #This line creates database which will contain all needed data

db = SQLAlchemy(app) #db is an object of the SQLAlchemy class, which is created by passing the app instance to the SQLAlchemy constructor
class BlogPosts(db.Model): #This line creates class BlogPosts, which is the subclass of db object and inherits all its' attributes and methods
	__tablename__ = 'blog_posts' #This line creats table which is used to save out posts
	id = db.Column('id', db.Integer, primary_key = True) #id column
	text = db.Column(db.String(200000))  #posts column
	datetime = db.Column(db.DateTime()) #date and time column
	def __init__(self, text, datetime): #we are defining method which is used to initialize the object. Values text and datetime are assigned to variables with the same names
	   self.text = text
	   self.datetime = datetime

@app.route('/') #our home page
def hello(): #method which downloads the home page
    return render_template('index.html', utc_dt=datetime.now()) #This is an example of using variable from html part

@app.route('/save_data', methods=['POST']) #this is my way to save data from input form to database
def save_data():
    data=request.form['posts'] #we are collecting data which user entered to the form on a main page. posts is a name assigned to form in the HTML part.
    db.session.add(BlogPosts(text=data, datetime=datetime.now())) #so is one transaction with database to add text from user and to save information about date and time of entering those data
    db.session.commit() #saving changes
	#    with open('data.txt', 'a') as w: - previous way to save data
	#        w.write(data+'\n') - which used simple text file in the root directory of the project. Good old times.
    time.sleep(1) #just to make webpage a little bit more oldschool
	
    return redirect(url_for('hello')) #to refresh the home page after saving data

@app.route('/about_project') #just page 'about'
def about():
    return render_template('about.html') #basically just to show the text at the moment

@app.route('/blog_posts') #currently the second valuable page in the project
def posts():
	posts = BlogPosts.query.all() #so we assign posts to be the children of database. One raw in our table means one post
	print (posts) #this is so obvious, isn't it
	#    with open('data.txt','r') as f: - previous way to print data
	#        posts = [line.strip() for line in f.readlines()] - from the simple text file. Good old days.
	return render_template('posts.html', posts=posts) #of course, we need to show webpage after completing printing action. Why else would we write this method here?

if __name__ == "__main__": #this part I don't understand at the moment, but it must be here
	with app.app_context(): #to create a new application context in Flask app
		db.create_all() #to create needed tables if they aren't exist
	app.run(debug=True) #so app must work considering all part of code upside