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
from sistema.models import Usuario, Escola, Aluno, FuncionarioEscola, Projetos, Post, Empresa, FuncionarioEmpresa, Vagas, Indicacao # importar as tabelas do models

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
    nome = StringField('Nome da Escola', validators=[DataRequired()])
    localizacao = StringField('Localização da Escola', validators=[DataRequired()])
    contato = TextAreaField('Contato(s)', validators=[DataRequired()])
    btn_escola = SubmitField('Cadastrar')

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
    nome = StringField('Nome Aluno', validators=[DataRequired()])
    turma = SelectField('Turma', choices=['Regular', 'Tecnico'])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    contato = TextAreaField('Contato(s)', validators=[DataRequired()])
    escola = SelectField('Colegio', coerce=int, validators=[DataRequired()])
    btn_aluno = SubmitField('Cadastrar')

    # criando o validador
    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            raise ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro

    def save(self):
        # criptografando a senha
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        aluno = Aluno(
            nome = self.nome.data,
            turma = self.turma.data,
            email = self.email.data,
            senha = senha,
            contato = self.contato.data,
            id_colegio = self.escola.data
        )

        db.session.add(aluno)
        db.session.commit()

# formulario do funcionario_escola
class FuncionarioEscolaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cargo = SelectField('Cargo', choices=['Diretor', 'Vice-Diretor', 'Coordenador ou Pedagogo', 'Orientador Educacional', 'Professor/Docente', 'Supervisor Educacional', 'Auxiliar de Educação Especial / Cuidador', 'Psicopedagogo', 'Secretário Escolar', 'Inspetor de Alunos', 'Merendeiro', 'Equipe de Limpeza e Manutenção', 'Porteiro'])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    contato = TextAreaField('Contato(s)', validators=[DataRequired()])
    escola = SelectField('Escola', coerce=int, validators=[DataRequired()])
    btn_funcionario_escola = SubmitField('Cadastrar')
    
    # criando o validador
    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            raise ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro
        
    def save(self):
        # criptografando a senha
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        funcionario = FuncionarioEscola(
            nome = self.nome.data,
            cargo = self.cargo.data,
            email = self.email.data,
            senha = senha,
            contato = self.contato.data,
            id_colegio = self.escola.data
        )

        db.session.add(funcionario)
        db.session.commit()

# formulario de post
class PostForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    escola = SelectField('Selecione a Escola', coerce=int, validators=[DataRequired()])
    btn_post = SubmitField('Postar')
    
    def save(self):
        post = Post(
            titulo = self.titulo.data,
            descricao = self.descricao.data,
            id_escola = self.escola.data
        )
    
        # salvando no db
        db.session.add(post)
        db.session.commit()

# formulario da empresa
class EmpresaForm(FlaskForm):
    nome = StringField('Nome da Empresa', validators=[DataRequired()])
    localizacao = StringField('Localização', validators=[DataRequired()])
    contato = TextAreaField('Contato(s)', validators=[DataRequired()])
    btn_empresa = SubmitField('Cadastrar')

    def save(self):
        empresa = Empresa(
            nome = self.nome.data,
            localizacao = self.localizacao.data,
            contato = self.contato.data
        )

        db.session.add(empresa)
        db.session.commit()

# formulario do funcionario_empresa
class FuncionarioEmpresaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cargo = SelectField('Cargo', choices=['Proprietário / Dono', 'Sócio', 'Diretor', 'Gerente', 'Supervisor / Coordenador', 'Líder de Equipe', 'Funcionário / Colaborador', 'Atendente / Vendedor', 'Assistente / Auxiliar', 'Estagiário / Jovem Aprendiz', 'Terceirizado / Prestador de Serviços'], validators=[DataRequired()])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    contato = TextAreaField('Contato(s)', validators=[DataRequired()])
    empresa = SelectField('Empresa', coerce=int, validators=[DataRequired()])
    btn_funcionario_empresa = SubmitField('Cadastrar')

    # criando o validador
    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first(): # busca na tabela usuario, na coluna email, o email enviado
            raise ValidationError('Usuario já cadastrado com esse Email!!') # resposta do erro
        
    def save(self):
        # criptografando a senha
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        funcionario = FuncionarioEmpresa(
            nome = self.nome.data,
            cargo = self.cargo.data,
            email = self.email.data,
            senha = senha,
            contato = self.contato.data,
            id_empresa = self.empresa.data
        )

        db.session.add(funcionario)
        db.session.commit()

# formulario de vagas
class VagasForm(FlaskForm):
   titulo = StringField('Titulo da Vaga', validators=[DataRequired()])
   descricao = TextAreaField('Descrição da Vaga', validators=[DataRequired()])
   empresa = SelectField('Empresa responsavel', coerce=int, validators=[DataRequired()])
   btn_vaga = SubmitField('Postar') 

   def save(self):
       vaga = Vagas(
           titulo = self.titulo.data,
           descricao = self.descricao.data,
           id_empresa = self.empresa.data
       )

       db.session.add(vaga)
       db.session.commit()

# formulario de indicação
class IndicacaoForm(FlaskForm):
    status = SelectField('Qual tipo de inscrição?', choices=['Candidatar-se', 'Indicar'] ,validators=[DataRequired()])
    escola = SelectField('Qual sua Escola?', validators=[DataRequired()])
    indicado = SelectField('Quem vai ser indicado?', coerce=int, default=None)
    vaga = SelectField('Qual a vaga escolhida?', validators=[DataRequired()])
    btn_indicacao = SubmitField('Indicar')
    btn_candidatar = SubmitField('Candidatar-se')

    def save(self, aluno_logado_id=None):
        id_aluno_final = self.indicado.data
        
        # Se for auto-candidatura, o ID do aluno é o do próprio usuário logado
        if self.status.data == 'Candidatar-se' and aluno_logado_id:
            id_aluno_final = aluno_logado_id

        indicacao = Indicacao(
            status=self.status.data,
            id_escola=self.escola.data,
            id_vaga=self.vaga.data,
            id_aluno=id_aluno_final
        )

        db.session.add(indicacao)
        db.session.commit()

# formulario de projetos
class ProjetosForm(FlaskForm):
    titulo = StringField('Titulo do Projeto', validators=[DataRequired()])
    descricao = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    imagem = FileField('Imagem do Projeto', validators=[FileRequired('A imagem é obrigatória!'), FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens são permitidas!')])
    escola = SelectField('Escola', coerce=int, validators=[DataRequired()])
    btn_projetos = SubmitField('Salvar')

    def save(self):
        imagem = self.imagem.data
        nome_seguro = secure_filename(imagem.filename)

        # USANDO O RECURSO NATIVO DO FLASK:
        # app.root_path aponta direto para a pasta interna do seu app (onde fica a pasta 'static')
        # Se a sua pasta 'static' estiver na raiz do projeto, usamos os.path.dirname(app.root_path)
        
        # Vamos criar um print temporário para você ver no terminal onde ele está salvando
        caminho_base = app.root_path
        if not os.path.exists(os.path.join(caminho_base, 'static')):
            caminho_base = os.path.dirname(app.root_path)

        caminho_completo = os.path.join(
            caminho_base,
            'static',
            'data',
            'projetos',
            nome_seguro
        )

        # Imprime no terminal do VS Code o local exato onde o Python vai gravar o arquivo
        print("====== CAMINHO REAL DE SALVAMENTO ======")
        print(caminho_completo)
        print("========================================")

        # Garante a criação física dos diretórios no Windows
        os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)

        # Salva o arquivo físico no lugar correto
        imagem.save(caminho_completo)

        # Salva no Banco de Dados
        projeto = Projetos(
            titulo=self.titulo.data,
            descricao=self.descricao.data,
            id_escola=self.escola.data,
            imagem=nome_seguro
        )
        
        db.session.add(projeto)
        db.session.commit()