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
    empresa = db.relationship('Empresa', backref="user_empresa", uselist=False, lazy=True)
    escola = db.relationship('Escola', backref="user_escola", uselist=False, lazy=True)
    
### ---------Hierarquia Empresa--------- ###
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = True)
    localizacao = db.Column(db.String(100), nullable = True)
    contato = db.Column(db.String(100), nullable = True)
    
    # chave estrangeira de login
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    # relacionamento 
    funcionario = db.relationship('Funcionario', backref="empresa_funcionario", lazy=True)

    # relacionamento de posts.vagas para empresa
    post = db.relationship('Post', backref="empresa_post", lazy=True)

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

    # chave estrangeira de login
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

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

    # relacionamento de aluno para inscrito
    candidato = db.relationship('Inscrito', backref="aluno_candidato", lazy=True, )

### ------------tabela post------------ ###
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = True)
    autor = db.Column(db.String(100), nullable = True)
    tipo = db.Column(db.String(50), nullable = True)
    mensagem = db.Column(db.Text, nullable = True)
    
    # se for do tipo vaga tera prazo
    validade = db.Column(db.DateTime, nullable = True)
    
    # relacionamento com filtro no tipo = 'vagas'
    candidato = db.relationship('Inscrito', backref="inscrito_post", lazy=True)
    
    # relacionamento com filto no tipo = 'projeto'
    projetos = db.relationship('Projeto', backref="projeto_post", lazy=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))

### ------------tabela inscrito------------ ###
class Inscrito(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    # chave estrangeira de vagas
    post_id = db.Column(db.ForeignKey('post.id'))

    # chave estrangeira de alunos 
    indicado = db.Column(db.ForeignKey('aluno.id'))

    # chave estrangeira de empresa
    empresa = db.Column(db.ForeignKey('empresa.id') )

    inscrito = db.Column(db.String(100), nullable = True)

    # info do candidato
    curriculo = db.Column(db.Text, nullable = True)

    
### ------------tabela Projeto------------ ###
class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    arquivo = db.Column(db.String(200), nullable = True)
    imagem = db.Column(db.String(200), nullable = True)

    # chave estrangeira de post
    post_id = db.Column(db.ForeignKey('post.id'))
    
    
# Colocar cnpj em empresa e escola -> cnpj = db.Column(db.String(14))