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
from sistema.models import Usuario, Escola, Aluno, FuncionarioEscola, Projetos, Post, Empresa, FuncionarioEmpresa, Vagas # importar as tabelas do models

# biblioteca usada pra salvar arquivo 
import os

# segurança no bd
from werkzeug.utils import secure_filename

# formulario de cadastro
class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    categoria = SelectField('Escolha uma Categoria', choices=['Aluno', 'Admin', 'Escola', 'Empresa', 'Funcionario/Escola', 'Funcionario/Empresa'])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    btnsubmit = SubmitField('Salvar')

    # criando o validador
    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            raise ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro

    def validate_nome(self, nome): 
        if self.categoria.data.lower() == 'admin':
            if Usuario.query.filter(Usuario.nome.ilike('admin')).first():
                raise ValidationError('Admin já cadastrado no sistema!!!')

        if self.categoria.data == 'Empresa':
            if Usuario.query.filter(Usuario.nome.like(nome.data)).first():
                raise ValidationError('Empresa já cadastrada com esse nome!!!')
        
    # criando o save
    def save(self):
        # criptografando a senha
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        # criando o usuario
        usuario = Usuario(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha,
            categoria = self.categoria.data
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
    pass

# formulario do aluno
class AlunoForm(FlaskForm):
    pass

# formulario do funcionario_escola
class FuncionarioEscolaForm(FlaskForm):
    pass

# formulario de projetos
class ProjetosForm(FlaskForm):
    pass

# formulario de post
class PostForm(FlaskForm):
    pass

# formulario da empresa
class EmpresaForm(FlaskForm):
    pass

# formulario do funcionario_empresa
class FuncionarioEmpresaForm(FlaskForm):
    pass

# formulario de vagas
class VagasForm(FlaskForm):
   pass