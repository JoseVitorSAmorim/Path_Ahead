# importando a classe do pacote
from flask_wtf import FlaskForm

# importando o current app para pegar a pasta raiz
from flask import current_app, request

# importando o tipo de campo e os validators
from wtforms import StringField, EmailField, PasswordField, SubmitField, PasswordField, IntegerField, SelectField, TextAreaField, DateTimeField

# importando os campos de arquivo
from flask_wtf.file import FileField, FileAllowed, FileRequired, MultipleFileField

# importando os validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# importando as tabelas e o db
from sistema import db, bcrypt, app
from sistema.models import Usuario, Empresa, Aluno, Escola, Funcionario, Post, Inscrito, Projeto # importar as tabelas do models

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
    btn_cadastro = SubmitField('Salvar')

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
    btn_login = SubmitField('Enviar')

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

class EmpresaForm(FlaskForm):
    nome = StringField('Nome da Empresa')
    localizacao = StringField('Localização')
    contato = TextAreaField('Contatos')
    btn_empresa = SubmitField('Cadastrar')
    
    def save(self, id_user):
        nova_empresa = Empresa(
            nome=self.nome.data,
            localizacao=self.localizacao.data,
            contato=self.contato.data,
            usuario_id=id_user
        )
        db.session.add(nova_empresa)
        db.session.commit()
        return nova_empresa
    
class EscolaForm(FlaskForm):
    nome = StringField('Nome da Escola')
    localizacao = StringField('Localização')
    contato = TextAreaField('Contatos')
    btn_escola = SubmitField('Cadastrar')

    def save(self, id_user):
        nova_escola = Escola(
            nome=self.nome.data,
            localizacao=self.localizacao.data,
            contato=self.contato.data,
            usuario_id=id_user
        )
        db.session.add(nova_escola)
        db.session.commit()
        return nova_escola

class AlunoForm(FlaskForm):
    turma = StringField('Turma')
    descricao = TextAreaField('Descrição do aluno')
    escola = SelectField('Escola do Aluno', coerce=int)
    btn_aluno = SubmitField('Cadastrar')

    def save(self, id_user):
        novo_aluno = Aluno( 
            turma=self.turma.data,
            descricao=self.descricao.data,
            escola_id=self.escola.data,
            usuario_id=id_user
        )

        db.session.add(novo_aluno)
        db.session.commit()

        return novo_aluno

class FuncionarioForm(FlaskForm):
    escola = SelectField('Escola do funcionario', coerce=int)
    empresa = SelectField('Empresa do funcionario', coerce=int)
    btn_funcionario = SubmitField('Cadastrar')

    def save(self, id_user):
        # Converte o valor 0 (caso escolha "Nenhum") para None
        escola_id = self.escola.data if self.escola.data != 0 else None
        empresa_id = self.empresa.data if self.empresa.data != 0 else None
        
        novo_funcionario = Funcionario(
            usuario_id=id_user,
            escola_id=escola_id,
            empresa_id=empresa_id
        ) 
        db.session.add(novo_funcionario)
        db.session.commit()
        return novo_funcionario

class PostForm(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired()])
    tipo = SelectField('Categoria da Postagem', choices=[('postagem', 'Postagem'), ('vagas', 'Vagas'), ('projeto', 'Projeto')], validators=[DataRequired()])
    mensagem = TextAreaField('Conteudo da Postagem', validators=[DataRequired()])
    prazo = DateTimeField('Defina o Prazo')
    btn_post = SubmitField('Enviar')

    def save(self, current_user_id):
        novo_post = Post(
            titulo = self.titulo.data,
            autor = current_user_id,
            tipo = self.tipo.data,
            mensagem = self.mensagem.data,
            validade = self.prazo.data
        )

        db.session.add(novo_post)
        db.session.commit()

        return novo_post
    
class InscricaoForm(FlaskForm):
    empresa = SelectField('Selecione uma empresa', coerce=int)
    vaga = SelectField('Selecione uma vaga', coerce=int)
    aluno = SelectField('Selecione um aluno', coerce=int)
    btn_indicar = SubmitField('Indicar')
    btn_inscrever = SubmitField('Inscrever-se')

    # apos escolher a inscrição esse label aparece
    dados = TextAreaField('Coloque suas informações')
    
    # se o aluno se inscrever 
    def save_inscrito(self, current_user_id):
        novo_inscrito = Inscrito(
            empresa = self.empresa.data,
            post_id = self.vaga.data,
            inscrito = current_user_id,
            curriculo = self.dados.data
        )

        db.session.add(novo_inscrito)
        db.session.commit()

        return novo_inscrito
    
    # se o aluno for indicado
    def save_indicado(self):
        novo_indicado = Inscrito(
            empresa = self.empresa.data,
            post_id = self.vaga.data,
            indicado = self.aluno.data,
        )

        db.session.add(novo_indicado)
        db.session.commit()

class Projetos(FlaskForm):
    imagem = FileField('Imagem do Projeto', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens!')])
    arquivos_pasta = MultipleFileField('Arquivos da Pasta')

    btn_projeto = SubmitField('Enviar')

    def save(self, post_id_vinculado):
        nome_imagem_salva = None
        caminho_pasta_salva = None

        # 1. Processa e salva a Imagem Única
        if self.imagem.data:
            arquivo_img = self.imagem.data
            # Gera um nome seguro incluindo o ID do post para evitar duplicatas
            nome_img_seguro = secure_filename(f"projeto_{post_id_vinculado}_{arquivo_img.filename}")
            caminho_img = os.path.join(current_app.config['UPLOAD_FOLDER'], 'imagens', nome_img_seguro)
            arquivo_img.save(caminho_img)
            nome_imagem_salva = nome_img_seguro

        # 2. Processa e salva a Pasta de Arquivos
        # Pegamos a lista real de múltiplos arquivos enviados via request
        arquivos = request.files.getlist('arquivos_pasta')
        
        # Verifica se pelo menos um arquivo válido foi enviado
        if arquivos and arquivos[0].filename != '':
            # Cria uma pasta exclusiva para este projeto no servidor
            nome_pasta_projeto = f"arquivos_projeto_{post_id_vinculado}"
            caminho_diretorio_projeto = os.path.join(current_app.config['UPLOAD_FOLDER'], 'projetos', nome_pasta_projeto)
            os.makedirs(caminho_diretorio_projeto, exist_ok=True)

            for arquivo in arquivos:
                if arquivo.filename == '':
                    continue
                
                # Extrai apenas o nome final do arquivo para segurança
                nome_arq_seguro = secure_filename(os.path.basename(arquivo.filename))
                caminho_final_arquivo = os.path.join(caminho_diretorio_projeto, nome_arq_seguro)
                arquivo.save(caminho_final_arquivo)
            
            # Caminho relativo que será guardado no banco de dados para fácil acesso depois
            caminho_pasta_salva = os.path.join('uploads', 'projetos', nome_pasta_projeto)

        # 3. Cria e salva o registro na tabela Projeto do Banco de Dados
        novo_projeto = Projeto(
            imagem = nome_imagem_salva,
            arquivo = caminho_pasta_salva,
            post_id = post_id_vinculado
        )
        
        db.session.add(novo_projeto)
        db.session.commit()
        
        return novo_projeto