from sistema import db, login_manager
from datetime import datetime

# Classe usada para informar em qual modelo vai utilizar para fazer login do usuario
from flask_login import UserMixin

# recuperando o usuario
@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(int(user_id))

# entidade de cadastro
class Usuario(db.Model, UserMixin): # essa tabela vai ter o login
    id = db.Column(db.Integer, primary_key = True) 
    nome = db.Column(db.String(200), nullable = True)
    sobrenome = db.Column(db.String(200), nullable = True)
    email = db.Column(db.String(200), nullable = False, unique = True)
    senha = db.Column(db.String(200), nullable = False)
    categoria = db.Column(db.String(200), nullable= False) # status - aluno, escola, empresa, funcionario
    
# Entidade Pai - Escola
class Escola(db.Model):
    id = db.Column()
    nome = db.Column()
    localizacao = db.Column()
    contato = db.Column()
    # relacionamento de escola com aluno
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable = False) # 1 -> relacionar com a tabela aluno
    # relacionamento de escola com funcionario
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario_escola.id'), nullable = False) # 2 -> relacionar com a tabela funcionario
    # relacionar escola com projetos
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable = False) # 3 -> relacionar escola projetos

# entidade filho - Escola/aluno
class Aluno(db.Model):
    id = db.Column(db.Integer, primari_key = True )
    nome = db.Column(db.String(100), nullable = False)
    # realacao aluno com colegio
    id_colegio = db.relationship('Escola', backref = 'aluno_escola', lazy = True, cascade='all, delete-orphan') # 1 -> relacionado aluno escola
    turma = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    senha = db.Column(db.String(100), nullable = False)
    contato = db.Column(db.Text, nullable = False) 

# entidade filho - Escola/funcionario
class Funcionario_Escola(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    nome = db.Column(db.String(100), nullable = False )
    # relacionamento da escola com o funcionario
    id_colegio = db.relationship('Escola.id', backref = 'funcionario_escola', lazy = True, cascade='all, delete-orphan') # 2 -> relacionado funcionario escola
    cargo = db.Column(db.String(100), nullable = False )
    email = db.Column(db.String(100), nullable = False )
    senha = db.Column(db.String(100), nullable = False)
    contato = db.Column(db.Text, nullable = False)

# entidade filho / table_intermediaria - Escola/projetos
class Projetos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.Text, nullable = False)
    data_postagem = db.Column(db.Date, datetime.utcnow)
    imagem = db.Column(db.String, nullable = True)
    # relacionamento de escola com projetos
    id_escola = db.relationship('Escola', backref = 'escola_projeto', lazy = True, cascade='all, delete-orphan') # 3 -> relacionar escola com projetos
    

# entidade filho / table_intermediaria - Escola/post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.Text, nullable = False)
    data_postagem = db.Column(db.Date, datetime.utcnow)
    # relacionamento de escola com post
    id_escola = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable = False)

# Entidade Pai - Empresa
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    localizacao = db.Column(db.String(150), nullable = False)
    contato = db.Column(db.Text, nullable = False)
    # criar o relation ship do funcionario com a empresa
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario_empresa.id'), nullable = False) # 5 -> relacionar funcionario empresa com empresa
    # relacionar empresa com vagas
    id_vagas = db.Column(db.Integer, db.ForeignKey('vagas'), nullable = False) # 6 -> relacionar empresa com vagas

# entidade filho - Empresa/funcionario
class Funcionario_Empresa(db.Model):
    id = db.Column(db.Integer, primari_key = True)
    nome = db.Column(db.String(100), nullable = False)
    # relacionamento do funcionario com a empresa
    empresa = db.relationship('Empresa', backref = 'funcionario_empresa', lazy = True, cascade='all, delete-orphan')
    cargo = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    senha = db.Column(db.String(100), nullable = False)
    contato = db.Column(db.String(100), nullable = False)

# entidade Função - processo (2)
class Indicacao(db.Model):
    id = db.Column(db.Integer, primari_key = True)
    # estrutura da escola
    id_escola = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable = False) # 7 -> relacionar indicação com escola
    status = db.Column(db.String(20), nullable = False) # se for inscrito ou indicado, nao precisa ser bool necessariamente
    # relacionamento de vagas com indicação
    vagas = db.relationship('Vagas', backref = 'indicacao_vagas', lazy = True, cascade='all, delete-orphan')
    
# entidade Função - processo (1)
class Vagas(db.Model):
    id = db.Column(db.Integer, primari_key = True )
    titulo = db.Column()
    descricao = db.Column()
    # relacionamento de indicação com vagas
    id_indicacao = db.Column(db.Integer, db.ForeignKey('Indicacao'), nullable = True) # 8 -> relacionar indicacao com vagas
    # relacionamento de funcionario_empresa com vagas
    empresa = db.relationship('Empresa', backref = 'empresa_vagas', lazy = True, cascade='all, delete-orphan') # 6 -> relacionado

