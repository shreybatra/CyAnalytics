from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileRequired, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class UploadForm(FlaskForm):
	csv = FileField('Choose csv', validators=[FileRequired()])
	filename = StringField('Filename', validators=[DataRequired()])
	submit = SubmitField('Upload File')

class LoadForm(FlaskForm):
	pass

class SelectForm(FlaskForm):
	submit = SubmitField('Select Data?')

class ChartButtonForm(FlaskForm):
	submit = SubmitField('Analyse?')