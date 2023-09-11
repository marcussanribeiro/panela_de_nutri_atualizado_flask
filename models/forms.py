from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, DateTimeField, DateTimeLocalField, TextAreaField, SubmitField, SelectField, FileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput


class loginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])



class registerForm(FlaskForm):
    cargos = [("Usuario", "Usuario")]
    nome = StringField('nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome')
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    funcao = SelectField('função', choices=cargos, validators=[DataRequired()])

class postForm(FlaskForm):
    arquivo = FileField("Selecionar Arquivo", validators=[FileAllowed(['png', 'jpg'])])
    enviar = SubmitField('Enviar')

class UploadForm(FlaskForm):
    nome = StringField('Nome', validators=[FileRequired()])
    descricao = StringField('Descrição')
    arquivo = FileField('Selecionar arquivo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    enviar = SubmitField('Enviar')