from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import case, cast, String, and_
from flask import Flask, render_template, request, redirect, url_for
import time
from datetime import datetime

app = Flask(__name__, static_folder='static') #This line must be in every similar app. We also need to assign static folder to avoid browsers' cybersecurity settings.
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3' #This line creates database which will contain all needed data
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #This line will refresh the DB with every launch to make sure that uodated code works well

db = SQLAlchemy(app) #db is an object of the SQLAlchemy class, which is created by passing the app instance to the SQLAlchemy constructor
class BlogPosts(db.Model): #This line creates class BlogPosts, which is the subclass of db object and inherits all its' attributes and methods
	__tablename__ = 'blog_posts' #This line creats table which is used to save out posts
	id = db.Column('id', db.Integer, primary_key = True) #id column
	title = db.Column (db.String(200)) #titles' column
	text = db.Column(db.String(200000))  #posts' column
	datetime = db.Column(db.DateTime()) #date and time column
	likes = db.Column('likes', db.Integer, default=0)
	dislikes = db.Column('dislikes', db.Integer, default=0)
	def __init__(self, title, text, datetime): #we are defining method which is used to initialize the object. Values text and datetime are assigned to variables with the same names
	   self.title = title
	   self.text = text
	   self.datetime = datetime
	   
@app.route('/') #our home page
def hello(): #method which downloads the home page
    return render_template('index.html', utc_dt=datetime.now().replace(microsecond=0)) #This is an example of using variable from html part

@app.route('/save_data', methods=['POST']) #this is my way to save data from input form to database
def save_data():
	datat=request.form['titles'] #to collect titles
	data=request.form['posts'] #we are collecting data which user entered to the form on a main page. posts is a name assigned to form in the HTML part.
	db.session.add(BlogPosts(title = datat, text=data, datetime=datetime.now().replace(microsecond=0))) #so is one transaction with database to add text from user and to save information about date and time of entering those data
	db.session.commit() #saving changes
	#    with open('data.txt', 'a') as w: - previous way to save data
	#        w.write(data+'\n') - which used simple text file in the root directory of the project. Good old times.
	time.sleep(1) #just to make webpage look like a little bit more oldschool
	
	return redirect(url_for('hello')) #to refresh the home page after saving data

@app.route('/about_project') #just page 'about'
def about():
    return render_template('about.html') #basically just to show the text at the moment

@app.route('/blog_posts', methods=['GET', 'POST']) #currently the second valuable page in the project. I added get method because I need it after adding likes and dislikes to receive information
def posts():
	posts = BlogPosts.query.all() #so we assign posts to be the children of database. One raw in our table means one post
	print (posts) #this is so obvious, isn't it
	#    with open('data.txt','r') as f: - previous way to print data
	#        posts = [line.strip() for line in f.readlines()] - from the simple text file. Good old days.
	return render_template('posts.html', posts=posts) #of course, we need to show webpage after completing printing action. Why else would we write this method here?


@app.route('/like_posts', methods=['GET', 'POST'])
def like_post():
	if request.method == 'POST':
		post_id = request.form['like']
		post = BlogPosts.query.filter_by(id=post_id).first()
		post.likes += 1
		db.session.commit()
	return redirect(url_for('posts'))

@app.route('/dislike_posts', methods=['GET','POST'])
def dislike_post():
	if request.method == 'POST':
		post_id = request.form['dislike']
		post = BlogPosts.query.filter_by(id=post_id).first()
		post.dislikes += 1
		db.session.commit()
	return redirect (url_for('posts'))

if __name__ == "__main__": #this part I don't understand at the moment, but it must be here
	with app.app_context(): #to create a new application context in Flask app
                db.create_all() #to create needed tables if they aren't exist but somehow this doesn't work - learn that question after
	app.run(debug=True) #so app must work considering all part of code upside
