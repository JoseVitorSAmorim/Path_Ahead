from sistema import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# recuperando o usuario
@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(int(user_id))

### ----------Usuario---------- ###
# tabela de usuario que define os acessos
class Usuario(db.Model, UserMixin): # essa tabela vai ter o login
    id = db.Column(db.Integer, primary_key = True) 
    nome = db.Column(db.String, nullable = True)
    sobrenome = db.Column(db.String, nullable = True)
    email = db.Column(db.String, nullable = True, unique = True)
    senha = db.Column(db.String, nullable = True)

    # coluna de perfil
    perfil = db.Column(db.String, nullable = True) # aluno, empresa, funcionario, escola.

    # relacionamento
    funcionario = db.relationship('Funcionario', backref='user_funcionario', uselist=False, lazy = True)
    aluno = db.relationship('Aluno', backref="user_aluno", uselist=False, lazy=True)

### ---------Hierarquia Empresa--------- ###
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = True)
    localizacao = db.Column(db.String(100), nullable = True)
    contato = db.Column(db.String(100), nullable = True)

    # relacionamento 
    funcionario = db.relationship('Funcionario', backref="empresa_funcionario", lazy=True)

### -----------Tabela de funcionario base----------- ###
class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    # chave estrangeira de login
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    # chave estrangeira de empresa ou escola
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'))

### -----------Hierarquia Escola---------- ###
class Escola(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = True)
    localizacao = db.Column(db.String(100), nullable = True)
    contato = db.Column(db.String(100), nullable = True)

    # relacionamento
    funcionario = db.relationship('Funcionario', backref="escola_funcinario", lazy=True)
    aluno = db.relationship('Aluno', backref="escola_aluno", lazy=True)

### ------------tabela aluno------------ ###
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    turma = db.Column(db.String(30), nullable = True)
    descricao = db.Column(db.Text, nullable = True)

    # chave estrangeira de login
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    # chave estrangeira escola
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'))
