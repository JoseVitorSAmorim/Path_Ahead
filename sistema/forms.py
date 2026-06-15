# importando a classe do pacote
from flask_wtf import FlaskForm

# importando o current app para pegar a pasta raiz
from flask import current_app

# importando o tipo de campo e os validators
from wtforms import StringField, EmailField, PasswordField, SubmitField, PasswordField, IntegerField, SelectField, TextAreaField

# importando os campos de arquivo
from flask_wtf.file import FileField, FileAllowed, FileRequired

# importando os validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# importando as tabelas e o db
from sistema import db, bcrypt, app
from sistema.models import Usuario # importar as tabelas do models

# biblioteca usada pra salvar arquivo 
import os

# segurança no bd
from werkzeug.utils import secure_filename

# criando um formulario
class Geral(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    btn_nome = SubmitField('Enviar')
