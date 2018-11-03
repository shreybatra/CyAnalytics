from flask import Flask, render_template, request, flash,redirect
from config import Config

from forms import LoginForm, UploadForm

from pymongo import MongoClient

client = MongoClient()
db = client.cyanalytics
users = db.users


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
		pass

	return render_template('upload_load.html', title='Dashboard', heading='CyAnalytics', form=form, logged_in=True)






if __name__=='__main__':
	app.run(debug=True, use_reloader=True, port=5000)