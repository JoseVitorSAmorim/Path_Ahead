# importando o aplicativo, db (banco)
from sistema import app, db

# importando a função render_template, url_for
from flask import render_template, url_for, request, redirect, flash

# importando as dependencias de login
from flask_login import login_user, logout_user, current_user, login_required

# importando a classe da tabela onde vou salvar
from sistema.models import Usuario, Aluno, Empresa, Escola, Funcionario, Post

# importando as classes de formulario
from sistema.forms import CadastroForm, LoginForm, AlunoForm, EscolaForm, EmpresaForm, FuncionarioForm, PostForm, InscricaoForm

# importando o operador logico "OR"
from sqlalchemy import or_

# criando rota de login
@app.route('/', methods=['GET', 'POST'])
def Login():
    # criando o bloco de login
    form_cadastro = CadastroForm()
    form_login = LoginForm()

    # verificando o login
    if form_login.validate_on_submit() and 'btnsubmit' in request.form:
        user = form_login.login()

        if user:
            login_user(user, remember=True)
            return redirect(url_for('Menu'))
        else:
            flash('E-mail ou Senha incorretos!!', 'danger')
    
    # buscando os dados
    escolas = Escola.query.all()
    empresas = Empresa.query.all()

    # instanciando os formularios
    form_aluno = AlunoForm()
    form_funcionario = FuncionarioForm()
    form_escola = EscolaForm()
    form_empresa = EmpresaForm()

    # abastecendo choices dos formularios
    form_aluno.escola.choices = [(escola.id, escola.nome) for escola in escolas]
    form_funcionario.escola.choices = [(escola.id, escola.nome) for escola in escolas]
    form_funcionario.empresa.choices = [(empresa.id, empresa.nome) for empresa in empresas]
    
    # PROCESSO: Executar Cadastro Completo e Dinâmico
    if form_cadastro.validate_on_submit() and 'nome' in request.form:
        perfil = form_cadastro.perfil.data
        
        # VALIDAÇÃO MANUAL: Garante que os campos dinâmicos não vieram vazios
        if perfil == 'aluno' and not form_aluno.turma.data:
            flash('O campo Turma é obrigatório para Alunos.', 'danger')
            return render_template('login.html', form_login=form_login, form_cadastro=form_cadastro, form_aluno=form_aluno, form_funcionario=form_funcionario, form_escola=form_escola, form_empresa=form_empresa)
        
        if perfil == 'empresa' and not form_empresa.nome.data:
            flash('O Nome da Empresa é obrigatório.', 'danger')
            return render_template('login.html', form_login=form_login, form_cadastro=form_cadastro, form_aluno=form_aluno, form_funcionario=form_funcionario, form_escola=form_escola, form_empresa=form_empresa)

        # 1. Salva o usuário na tabela base (Gera o ID)
        novo_usuario = form_cadastro.save()
        
        if novo_usuario:
            # 2. Salva na respectiva tabela de perfil usando a ID gerada
            if perfil == 'aluno':
                form_aluno.save(id_user=novo_usuario.id)
            elif perfil == 'empresa':
                form_empresa.save(id_user=novo_usuario.id)
            elif perfil == 'escola':
                form_escola.save(id_user=novo_usuario.id)
            elif perfil == 'funcionario':
                form_funcionario.save(id_user=novo_usuario.id)
            # Loga o usuário criado e manda para o Menu/Feed
            login_user(novo_usuario, remember=True)
            return redirect(url_for('Menu'))
        else:
            flash('Erro ao criar usuário, tente novamente.', 'danger')

    if form_cadastro.errors:
        print("Erros no Cadastro:", form_cadastro.errors)
        
    return render_template('login.html', form_cadastro=form_cadastro, form_login=form_login, form_aluno=form_aluno, form_empresa=form_empresa, form_escola=form_escola, form_funcionario=form_funcionario)

# criando o logout(sair)
@app.route('/sair/')
@login_required
def Logout():
    logout_user()
    
    return redirect(url_for('Login'))

# criando o Menu
@app.route('/menu-feed', methods=['GET', 'POST'])
def Menu():
    # buscando os dados
    alunos = Aluno.query.all()
    posts = Post.query.all()

    ### instanciando os formularios ##
    form_post = PostForm()

    ### validando o formulario ###
    if form_post.validate_on_submit() and 'btn_post' in request.form:
        form_post.save(current_user.id)
    



    return render_template('menu.html', form_post=form_post, posts=posts)

