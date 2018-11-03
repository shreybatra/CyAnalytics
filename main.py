from flask import Flask, render_template, request, flash,redirect, session
from config import Config

from forms import LoginForm, UploadForm, SelectForm

from pymongo import MongoClient
import pandas as pd

from bson.code import Code

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
			# print(df.dtypes.
			col_info = []
			for x,y in zip(df.columns, df.dtypes.values):
				# print(x+'---'+str(y))
				col_info.append({'key':x,
					'value':str(y)})
			col = db[filename]
			col.insert_many(df.to_dict('records'))

			docs = len(list(col.find()))
			datasets.insert_one({
				'filename': filename,
				'col_info':col_info
				})

			flash('Uploaded successfully with {} documents'.format(docs))
			session['filename'] = filename
			return redirect('/dataset/dashboard')

	return render_template('upload_load.html', title='Dashboard', heading='CyAnalytics', form=form, logged_in=True)


@app.route('/dataset/dashboard', methods=['GET','POST'])
def dataset_dashboard():



	# map_func = Code("function () {"
	# 				"for (var key in this) {emit(key, null);}"
	# 				"}"
	# 				)
	# reduce_func = Code("function (key, stuff) {return null; }")

	# result = db.iri.map_reduce(map_func, reduce_func, "myresults")

	# ans = result.find().distinct("_id")
	# ans =list(ans)

	ans = list(datasets.find({
		'filename':session['filename']
		}))[0]

	print(ans['col_info'])

	query_obj = []# [{item['key']: None} for item in ans['col_info']]

	for item in ans['col_info']:
		count = len(list(db.session['filename'].find({item['key']: None})))
		obj ={}
		obj['key'] = item['key']
		obj['count'] = count
		query_obj.append(obj)

	print(query_obj)



	# result = db.session['filename'].find(query_obj)

	# print(list(result))
	selectform = SelectForm()

	return render_template('dataset_dashboard.html', cols = ans['col_info'], missing=query_obj, select=selectform)


if __name__=='__main__':
	app.run(debug=True, use_reloader=True, port=5000)