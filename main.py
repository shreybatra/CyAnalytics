from flask import Flask, render_template, request, flash,redirect
from config import Config

from forms import LoginForm, UploadForm

from pymongo import MongoClient
import pandas as pd

client = MongoClient()
db = client.cyanalytics
users = db.users
datasets = db.datasets


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', heading='CyAnalytics', logged_in=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		data = dict(request.form)
		
		username = data['username'][0]
		password = data['password'][0]

		user = users.find({
			'username':username,
			'password':password
		})

		if not list(user):
			flash('Invalid Login Credentials')
			return redirect('/login')
		else:
			flash('Login successful for {}'.format(
				form.username.data))
			return redirect('/dashboard')

	return render_template('login.html', title='Sign In', heading='CyAnalytics', form=form, logged_in=False)



@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
	form = UploadForm()

	if form.validate_on_submit():
		f = request.files['csv']
		filename = form.filename.data

		file = datasets.find({
			'filename':filename
		})

		if list(file):
			flash('FileName already present, choose another name.')
			return redirect('/dashboard')
		else:
			df = pd.read_csv(f, encoding='latin1')
			col = db[filename]
			col.insert_many(df.to_dict('records'))

			docs = len(list(col.find()))
			datasets.insert_one({
				'filename': filename
				})

			flash('Uploaded successfully with {} documents'.format(docs))
			return redirect('/dashboard')

	return render_template('upload_load.html', title='Dashboard', heading='CyAnalytics', form=form, logged_in=True)






if __name__=='__main__':
	app.run(debug=True, use_reloader=True, port=5000)