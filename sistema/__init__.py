# importando do pacote flask a classe Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# importando a biblioteca os
import os # serve de interação, é necessario

# carregando a biblioteca de ambiente virtual
from dotenv import load_dotenv

# carregando o arquivo
load_dotenv('.env') # esse arquivo pode ter qualquer nome

# carregando os arquivos do flasklogin e o bcrypt
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# startando o aplicativo
app = Flask(__name__) # ele vai iniciar o aplicativo com base nesse arquivo.

# definindo o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') # acessando variavel do ambiente virtual

# verificador do banco de dados 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# token de segurança
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # acessando as variaveis do ambiente virtual
# Naming Convention
from sqlalchemy import MetaData

# Define um padrão de nomes para as restrições do banco
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

# Inicialize o db passando essa convenção
db = SQLAlchemy(metadata=metadata)

# definindo a variavel do banco de dados
db = SQLAlchemy(app)

# definindo o app de migrate
migrate = Migrate(app, db)

# definindo o loginmanager
login_manager = LoginManager(app)

# definindo o Bcrypt
bcrypt = Bcrypt()

# definindo a view de login
login_manager.login_view = 'login' # alterar para pagina onde vai ter o login

# configurando para receber os uploads
app.config['UPLOAD_FILE'] = r"static/data"

# caso der erro de url importar a rota
from sistema.views import Menu # importar no final para nao gerar erro

# importanto a tabela 
from sistema.models import Usuario # importar a tabela do models