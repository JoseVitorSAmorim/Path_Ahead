# importando a classe do pacote
from flask_wtf import FlaskForm

# importando o tipo de campo e os validators
from wtforms import StringField, EmailField, PasswordField, SubmitField, PasswordField, IntegerField, SelectField

# importando os campos de arquivo
from flask_wtf.file import FileField, FileAllowed

# importando os validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# importando as tabelas e o db
from sistema import db, bcrypt, app
from sistema.models import Usuario, Escola, Aluno, Funcionario_Escola, Projetos, Post, Empresa, Funcionario_Empresa, Vagas # importar as tabelas do models

# biblioteca usada pra salvar arquivo 
import os

# segurança no bd
from werkzeug.utils import secure_filename

# formulario de cadastro
class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    btnsubmit = SubmitField('Salvar')

    # criando o validador
    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            return ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro

    # criando o save
    def save(self):
        # criptografando a senha
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        # criando o usuario
        usuario = Usuario(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )

        # salvando
        db.session.add(usuario)
        db.session.commit()

        # retorno o usuario para fazer login
        return usuario
    

# formulario de login
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnsubmit = SubmitField('Enviar')

    # função de logar
    def login(self):
        # recupera o usuario
        user = Usuario.query.filter_by(email=self.email.data).first()

        # verificando a senha
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                # retorna o usuario
                return user
            else:
                raise Exception("Senha incorreta!!")
        else:
            return None
        
# formulario da escola
class EscolaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    localizacao = StringField('Localização', validators=[DataRequired()])
    contato = StringField('Contato(s)', validators=[DataRequired()])
    btnsubmit = SubmitField('Enviar')

    def save(self):
        escola = Escola(
            nome = self.nome.data,
            localizacao = self.localizacao.data,
            contato = self.contato.data
        )

        db.session.add(escola)
        db.session.commit()

# formulario do aluno
class AlunoForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    id_colegio = SelectField('Informe o Colegio', validators=[DataRequired()]) # buscar todos os colegios cadastrados
    turma = StringField('Nome Completo', validators=[DataRequired()])
    email_aluno = StringField('Nome Completo', validators=[DataRequired()])
    senha_aluno = PasswordField('Nome Completo', validators=[DataRequired()])
    contatos = StringField('Nome Completo', validators=[DataRequired()])
    btnsubmit = SubmitField('Enviar')

    def validate_email(self, email):
        if Aluno.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            return ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha_aluno.data.encode('utf-8'))

        aluno = Aluno(
            nome_completo = self.nome_completo.data,
            id_colegio = self.id_colegio.data,
            turma = self.turma.data,
            email_aluno = self.email_aluno.data,
            senha_aluno = senha,
            contatos = self.contatos.data,
        )

        db.session.add(aluno)
        db.session.commit()

# formulario do funcionario_escola
class Funcionario_EscolaForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    id_colegio = SelectField('Informe o Colegio', validators=[DataRequired()]) # buscar todos os colegios cadastrados
    email_funcionario = StringField('Nome Completo', validators=[DataRequired()])
    senha_funcionario = PasswordField('Nome Completo', validators=[DataRequired()])
    contatos = StringField('Nome Completo', validators=[DataRequired()])
    btnsubmit = SubmitField('Enviar')

    def validate_email(self, email):
        if Funcionario_Escola.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            return ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro
    
    def save(self):
        senha = bcrypt.generate_password_hash(self.senha_funcionario.data.encode('utf-8'))

        funcionario = Funcionario_Escola(
            nome_completo = self.nome_completo.data,
            id_colegio = self.id_colegio.data,
            email_funcionario = self.email_aluno.data,
            senha_funcionario = senha,
            contatos = self.contatos.data,
        )

        db.session.add(funcionario)
        db.session.commit()

# formulario de projetos
class ProjetosForm(FlaskForm):
    titulo = StringField('Nome Completo', validators=[DataRequired()])
    imagem = FileField('Escolha o Arquivo', validators=[DataRequired()])
    descricao = StringField('Nome Completo', validators=[DataRequired()])
    id_aluno = SelectField('Informe o Colegio', validators=[DataRequired()]) # buscar todos os alunos cadastrados
    id_funcionario_escola = SelectField('Informe o Colegio', validators=[DataRequired()]) # buscar funcionarios os colegios cadastrados
    btnsubmit = SubmitField('Enviar')

    def save(self):
        projeto = Projetos(
            titulo = self.titulo.data,
            imagem = self.imagem.data,
            descricao = self.descricao.data,
            id_aluno = self.id_aluno.data,
            id_funcionario_escola = self.id_funcionario_escola.data
        )

        db.session.add(projeto)
        db.session.commit()

# formulario de post
class PostForm(FlaskForm):
    titulo = StringField('Nome Completo', validators=[DataRequired()])
    imagem = FileField('Escolha o Arquivo', validators=[DataRequired()])
    descricao = StringField('Nome Completo', validators=[DataRequired()])
    id_aluno = SelectField('Informe o Colegio', validators=[DataRequired()]) # buscar todos os alunos cadastrados
    id_funcionario_escola = SelectField('Informe o Colegio', validators=[DataRequired()]) # buscar funcionarios os colegios cadastrados
    id_projeto = SelectField('Informe o Projeto', validators=[DataRequired()]) # buscar todos os projetos cadastrados
    btnsubmit = SubmitField('Enviar')

    def save(self):
        post = Post(
            titulo = self.titulo.data,
            imagem = self.imagem.data,
            descricao = self.descricao.data,
            id_aluno = self.id_aluno.data,
            id_funcionario_escola = self.id_funcionario_escola.data,
            id_projetos = self.id_projeto.data
        )

        db.session.add(post)
        db.session.commit()

# formulario da empresa
class EmpresaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    localizacao = StringField('Localização', validators=[DataRequired()])
    contato = StringField('Contato(s)', validators=[DataRequired()])
    btnsubmit = SubmitField('Enviar')

    def save(self):
        empresa = Empresa(
            nome = self.nome.data,
            localizacao = self.localizacao.data,
            contato = self.contato.data
        )

        db.session.add(empresa)
        db.session.commit()

# formulario do funcionario_empresa
class Funcionario_EmpresaForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    id_empresa = SelectField('Informe a Empresa', validators=[DataRequired()]) # buscar todos as empresas cadastradas
    email_funcionario = StringField('Nome Completo', validators=[DataRequired()])
    senha_funcionario = PasswordField('Nome Completo', validators=[DataRequired()])
    contatos = StringField('Nome Completo', validators=[DataRequired()])
    btnsubmit = SubmitField('Enviar')

    def validate_email(self, email):
        if Funcionario_Empresa.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            return ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro
    
    def save(self):
        senha = bcrypt.generate_password_hash(self.senha_funcionario.data.encode('utf-8'))

        funcionario = Funcionario_Escola(
            nome_completo = self.nome_completo.data,
            id_empresa = self.id_colegio.data,
            email_funcionario = self.email_aluno.data,
            senha_funcionario = senha,
            contatos = self.contatos.data,
        )

        db.session.add(funcionario)
        db.session.commit()

# formulario de vagas
class VagasForm(FlaskForm):
    titulo = StringField('Nome Completo', validators=[DataRequired()])
    descricao = StringField('Nome Completo', validators=[DataRequired()])
    id_funcionario_empresa = SelectField('Informe o Funcionario', validators=[DataRequired()]) # buscar funcionarios da empresa cadastrados
    id_aluno = SelectField('Informe o Aluno', validators=[DataRequired()]) # buscar os alunos cadastrados
    btnsubmit = SubmitField('Enviar')

    def save(self):
        vaga = Vagas(
            titulo = self.titulo.data,
            descricao = self.descricao.data,
            id_funcionario = self.id_funcionario_empresa,
            id_aluno = self.id_aluno.data
        )

        db.session.add(vaga)
        db.session.commit()