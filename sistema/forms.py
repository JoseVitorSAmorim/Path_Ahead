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
from sistema.models import Usuario, Empresa, Aluno, Escola, Funcionario # importar as tabelas do models

# biblioteca usada pra salvar arquivo 
import os

# segurança no bd
from werkzeug.utils import secure_filename

# formulario de cadastro
class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    perfil = SelectField('Tipo de Usuario', choices=[('aluno', 'Aluno'), ('funcionario', 'Funcionário'), ('empresa', 'Empresa'), ('escola', 'Escola'), ('admin', 'Admin')] ,validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    btnsubmit = SubmitField('Salvar')

    # criando o validador
    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            raise ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro

    # criando o save
    def save(self):
        # criptografando a senha
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        # criando o usuario
        usuario = Usuario(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            perfil = self.perfil.data,
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

# formulario da empresa
class EmpresaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    localizacao = StringField('Localização', validators=[DataRequired()])
    contato = TextAreaField('Contatos', validators=[DataRequired()])
    btn_empresa = SubmitField('Cadastrar')
    
    # metodo save
    def save(self, id_user):
        nova_empresa = Empresa(
            nome = self.nome.data,
            localizacao = self.localizacao.data,
            contato = self.contato.data,
            usuario_id = id_user
        )

        db.session.add(nova_empresa)
        db.session.commit()

        return nova_empresa
    
# formulario escola
class EscolaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    localizacao = StringField('Localização', validators=[DataRequired()])
    contato = TextAreaField('Contatos', validators=[DataRequired()])
    btn_escola = SubmitField('Cadastrar')
    
    # metodo save
    def save(self, id_user):
        nova_escola = Escola(
            nome = self.nome.data,
            localizacao = self.localizacao.data,
            contato = self.contato.data,
            usuario_id = id_user
        )

        db.session.add(nova_escola)
        db.session.commit()

        return nova_escola

# formulario aluno
class AlunoForm(FlaskForm):
    turma = StringField('Turma', validators=[DataRequired()] )
    descricao = TextAreaField('Descrição do aluno', validators=[DataRequired()])
    escola = SelectField('Escola do Aluno', coerce=int, validators=[DataRequired()])
    btn_aluno = SubmitField('Cadastrar')

    def save(self, id_user):
        novo_aluno = Escola(
            turma = self.turma.data,
            descricao = self.descricao.data,
            escola_id = self.escola.data,
            usuario_id = id_user
        )

        db.session.add(novo_aluno)
        db.session.commit()

        return novo_aluno

# formulario funcionario
class FuncionarioForm(FlaskForm):
    escola = SelectField('Escola do funcionario', coerce=int)
    empresa = SelectField('Empresa do funcionario', coerce=int)
    btn_funcionario = SubmitField('Cadastrar')

    def save(self, id_user):
        if self.escola.data and self.empresa.data == None:
            raise ValidationError("Voce deve selecionar 1 das opções pelo menos...")
        
        novo_funcionario = Funcionario(
            usuario_id = id_user,
            escola_id = self.escola.data,
            empresa_id = self.empresa.data
        ) 
    
        db.session.add(novo_funcionario)
        db.session.commit()

        return novo_funcionario
    