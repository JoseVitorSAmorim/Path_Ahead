from sistema import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ==========================================
# 1. USUÁRIO (Autenticação)
# ==========================================
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(200), nullable=True)
    sobrenome = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(200), nullable=False) # aluno, escola, empresa, funcionario

# ==========================================
# 2. ESTRUTURA ESCOLA
# ==========================================
class Escola(db.Model):
    __tablename__ = 'escola'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    localizacao = db.Column(db.String(200), nullable=False)
    contato = db.Column(db.String(200), nullable=False)
    
    # Relacionamentos lógicos (Uma escola tem vários filhos)
    alunos = db.relationship('Aluno', backref='aluno_escola', lazy=True, cascade='all, delete-orphan')
    funcionarios = db.relationship('FuncionarioEscola', backref='funcionario_escola', lazy=True, cascade='all, delete-orphan')
    projetos = db.relationship('Projetos', backref='projeto_escola', lazy=True, cascade='all, delete-orphan')
    posts = db.relationship('Post', backref='post_escola', lazy=True, cascade='all, delete-orphan')
    indicacoes = db.relationship('Indicacao', backref='indicacao_escola', lazy=True, cascade='all, delete-orphan')

class Aluno(db.Model):
    __tablename__ = 'aluno'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.Text, nullable=False)
    
    # Chave estrangeira correta: o Aluno pertence a uma Escola
    id_colegio = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)

class FuncionarioEscola(db.Model):
    __tablename__ = 'funcionario_escola'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) 
    cargo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.Text, nullable=False)
    
    # Chave estrangeira correta: o Funcionário pertence a uma Escola
    id_colegio = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)

class Projetos(db.Model):
    __tablename__ = 'projetos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_postagem = db.Column(db.Date, default=datetime.utcnow)
    imagem = db.Column(db.String, nullable=False, default = 'default.png')
    
    # Chave estrangeira correta: o Projeto pertence a uma Escola
    id_escola = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_postagem = db.Column(db.Date, default=datetime.utcnow)
    
    # Chave estrangeira
    id_escola = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)

# ==========================================
# 3. ESTRUTURA EMPRESA
# ==========================================
class Empresa(db.Model):
    __tablename__ = 'empresa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(150), nullable=False)
    contato = db.Column(db.Text, nullable=False)
    
    # Relacionamentos lógicos (Uma empresa tem vários funcionários e vagas)
    funcionarios = db.relationship('FuncionarioEmpresa', backref='empresa_funcionario', lazy=True, cascade='all, delete-orphan')
    vagas = db.relationship('Vagas', backref='empresa_vagas', lazy=True, cascade='all, delete-orphan')

class FuncionarioEmpresa(db.Model):
    __tablename__ = 'funcionario_empresa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(100), nullable=False)
    
    # Chave estrangeira correta: o Funcionário pertence a uma Empresa
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)

# ==========================================
# 4. PROCESSOS (Vagas e Indicações)
# ==========================================
class Vagas(db.Model):
    __tablename__ = 'vagas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)  # Corrigido: adicionado tipo String
    descricao = db.Column(db.Text, nullable=False)     # Corrigido: adicionado tipo Text
    
    # Chave estrangeira: a Vaga pertence a uma Empresa
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    
    # Relacionamento lógico com indicações recebidas nesta vaga
    indicacoes = db.relationship('Indicacao', backref='vaga_indicada', lazy=True, cascade='all, delete-orphan')

class Indicacao(db.Model):
    __tablename__ = 'indicacao'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False) # inscrito, indicado, etc.
    
    # Chaves estrangeiras da tabela intermediária (Quem indicou e para qual vaga)
    id_escola = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)
    id_vaga = db.Column(db.Integer, db.ForeignKey('vagas.id'), nullable=False)
