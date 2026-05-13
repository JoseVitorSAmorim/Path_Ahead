from sistema import db, login_manager
from datetime import datetime

# Classe usada para informar em qual modelo vai utilizar para fazer login do usuario
from flask_login import UserMixin

# recuperando o usuario
@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(user_id)

# entidade de cadastro
class Usuario(db.Model, UserMixin): # essa tabela vai ter o login
    id = db.Column(db.Integer, primary_key = True) 
    nome = db.Column(db.String, nullable = True)
    sobrenome = db.Column(db.String, nullable = True)
    email = db.Column(db.String, nullable = False, unique = True)
    senha = db.Column(db.String, nullable = False)
    categoria = db.Column(db.String, nullable= False)

# Entidade Pai - Escola
class Escola(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    nome = db.Column(db.String, nullable = False)
    alunos = db.relationship('Aluno', backref="aluno", lazy=True, cascade="all, delete-orphan")

# entidade filho - Escola/aluno
class Aluno(db.model):
    id = db.Column(db.Integer, primary_key = True)
    nome_completo = db.Column(db.Integer, primary_key = True)
    id_colegio = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable = False)
    turma = db.Column(db.String, unique = True, nullable = False)
    email_aluno = db.Column(db.String, unique = True, nullable = False)
    senha_aluno = db.Column(db.String, nullable = False)
    contatos = db.Column(db.String, nullable = False) # esse campo deve receber uma lista de valores
    aluno_projeto = db.relationship('Projetos', backref="aluno_projeto", lazy=True, cascade="all, delete-orphan")
    aluno_post = db.relationship('Post', backref="aluno_post", lazy=True, cascade="all, delete-orphan")
    aluno_post = db.relationship('Indicacao', backref="aluno_indicacao", lazy=True, cascade="all, delete-orphan")

# entidade filho - Escola/funcionario
class Funcionario_Escola(db.model):
    id = db.Column(db.Integer, primary_key = True)
    nome_completo = db.Column(db.Integer, primary_key = True)
    id_colegio = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable = False)
    email_funcionario = db.Column(db.String, unique = True, nullable = False)
    senha_funcionario = db.Column(db.String, nullable = False)
    contatos = db.Column(db.String, nullable = False) # esse campo deve receber uma lista de valores
    funcionario_projeto = db.relationship('Projetos', backref="funcionario_projeto", lazy=True, cascade="all, delete-orphan")
    funcionario_post = db.relationship('Post', backref="funcionario_post", lazy=True, cascade="all, delete-orphan")
    funcionario_indicacao = db.relationship('Indicacao', backref="funcionario_indicacao", lazy=True, cascade="all, delete-orphan")
    funcionario_vagas = db.relationship('Vagas', backref="funcionario_vagas", lazy=True, cascade="all, delete-orphan")

# entidade filho / table_intermediaria - Escola/projetos
class Projetos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String, nullable = False)
    imagem = db.Column(db.String, nullable = False)
    descricao = db.Column(db.String, nullable = False)
    data = db.Column(db.Date, default = datetime.utcnow())
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable = False) 
    id_funcionario_escola = db.Column(db.Integer, db.ForeignKey('funcionario_escola.id', nullable = False)) 
    post = db.relationship('Post', backref="projeto_post", lazy=True, cascade="all, delete-orphan")

# entidade filho / table_intermediaria - Escola/post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String, nullable = False)
    imagem = db.Column(db.String, nullable = False)
    descricao = db.Column(db.String, nullable = False)
    data = db.Column(db.Date, default = datetime.utcnow())
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable = False) 
    id_funcionario_escola = db.Column(db.Integer, db.ForeignKey('funcionario_escola.id', nullable = False)) 
    id_projetos = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable = False)

# Entidade Pai - Empresa
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    nome = db.Column(db.String, nullable = False)
    localizacao = db.Column(db.String, nullable = False)
    contato = db.Column(db.String, nullable = False) # essa linha recebe uma lista de valores
    funcionarios = db.relationship('Funcionario_empresa', backref="funcionario", lazy=True, cascade="all, delete-orphan")

# entidade filho - Empresa/funcionario
class Funcionario_Empresa(db.model):
    id = db.Column(db.Integer, primary_key = True)
    nome_completo = db.Column(db.Integer, primary_key = True)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable = False)
    email_funcionario = db.Column(db.String, unique = True, nullable = False)
    senha_funcionario = db.Column(db.String, nullable = False)
    contatos = db.Column(db.String, nullable = False) # esse campo deve receber uma lista de valores

# entidade Função - processo (1)
class Vagas(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String, nullable = False)
    descricao = db.Column(db.String, nullable = False)
    id_indicacao = db.Column(db.Integer, db.ForeignKey('indicacao.id')) # 2
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario_empresa.id'), nullable = False)
    vagas_indicacao = db.relationship('Indicacao', backref="vagas_indicacao", lazy=True, cascade="all, delete-orphan")

# entidade Função - processo (2)
class Indicacao(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable = False)
    descricao = db.Column(db.String, nullable = False)
    id_vaga = db.Column(db.Integer, db.ForeignKey('vagas.id'), nullable = True)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario_empresa.id'), nullable = False)
    indicacao_vaga = db.relationship('Vaga', backref="incacao_vaga", lazy=True, cascade="all, delete-orphan")