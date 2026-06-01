# importando o aplicativo, db (banco)
from sistema import app, db

# importando a função render_template, url_for
from flask import render_template, url_for, request, redirect, flash

# importando as dependencias de login
from flask_login import login_user, logout_user, current_user, login_required

# importando a classe da tabela onde vou salvar
from sistema.models import Usuario, Escola, Aluno, FuncionarioEscola, Projetos, Post, Empresa, FuncionarioEmpresa, Vagas

# importando as classes de formulario
from sistema.forms import LoginForm, CadastroForm, VagasForm, PostForm, EmpresaForm, AlunoForm, EscolaForm, ProjetosForm, FuncionarioEscolaForm, FuncionarioEmpresaForm

# criando rota de login
@app.route('/', methods=['GET', 'POST'])
def Login():
    # criando o bloco de login
    form_cadastro = CadastroForm()
    form_login = LoginForm()

    # verificando o login
    if form_login.validate_on_submit():
        user = form_login.login()

        if user:
            login_user(user, remember=True)
            return redirect(url_for('Menu'))
        else:
            flash('E-mail ou Senha incorretos!!', 'danger')

        # verificando cadastro
        if form_cadastro.validate_on_submit():
            # se estiver aqui, já verificou se o email é ou não repetido
            user = form_cadastro.save()
            # se user não for vazio
            if user:
                login_user(user, remember=True)
                return redirect(url_for('Menu'))
            else:
                flash('Erro ao criar usuario, tente novamente.', 'danger')

    return render_template('login.html', form_cadastro=form_cadastro, form_login=form_login)

# criando o logout(sair)
@app.route('/sair/')
@login_required
def Logout():
    logout_user()
    
    return redirect(url_for('Login'))

# criando a rota menu
@app.route('/menu/', methods=['GET', 'POST'])
@login_required
def Menu(): 
    form_post = PostForm()
    form_escola = EscolaForm()
    form_empresa = EmpresaForm()
    form_aluno = AlunoForm()
    form_funcionario_escola = FuncionarioEscolaForm()
    form_funcionario_empresa = FuncionarioEmpresaForm()
    form_vagas = VagasForm()

    # buscando os post
    posts = Post.query.all()

    # buscando as escolas
    escolas = Escola.query.all()

    # buscando os alunos
    alunos = Aluno.query.all()

    # buscando as empresas 
    empresas = Empresa.query.all()

    # buscando os funcionarios escolas
    funcionarios_escola = FuncionarioEscola.query.all()

    # buscando os funcionarios empresas
    funcionarios_empresa = FuncionarioEmpresa.query.all()
    
    # buscando as vagas postadas
    vagas_postadas = Vagas.query.all()

    # abastecendo o choices do select field
    form_post.escola.choices = [(escola.id, escola.nome) for escola in escolas]

    # abastecendo o form aluno
    form_aluno.escola.choices = [(escola.id, escola.nome) for escola in escolas]

    # abastecendo o form funcionario/escola
    form_funcionario_escola.escola.choices = [(escola.id, escola.nome) for escola in escolas]

    # abastecendo o form funcionario/empresa
    form_funcionario_empresa.empresa.choices = [(empresa.id, empresa.nome) for empresa in empresas]

    # abastecendo o form vagas
    form_vagas.empresa.choices = [(empresa.id, empresa.nome) for empresa in empresas]

    if form_post.validate_on_submit():
        form_post.save()
        print('post criado com sucesso')
        return redirect(url_for('Menu'))
    
    if form_escola.validate_on_submit() and form_escola.btn_escola.data:
        form_escola.save()
        print('Escola cadastrada com sucesso')
        return redirect(url_for('Menu'))

    elif form_aluno.validate_on_submit():
        form_aluno.save()
        print('Aluno criado com sucesso')
        return redirect(url_for('Menu'))
    
    if form_empresa.validate_on_submit() and form_empresa.btn_empresa.data:
        form_empresa.save() # Chamado APENAS UMA VEZ
        print('Empresa cadastrada com sucesso')
        return redirect(url_for('Menu'))

    if form_funcionario_escola.validate_on_submit() and form_funcionario_escola.btn_funcionario_escola.data:
        form_funcionario_escola.save()
        print('Funcionario cadastrado na escola com sucesso')
        return redirect(url_for('Menu'))
    
    if form_funcionario_empresa.validate_on_submit() and form_funcionario_empresa.btn_funcionario_empresa.data:
        form_funcionario_empresa.save()
        print('Funcionario Cadastrado na empresa com sucesso')
        return redirect(url_for('Menu'))

    if form_vagas.validate_on_submit() and form_vagas.btn_vaga.data:
        form_vagas.save()
        print('Vaga postada com sucesso')
        return redirect(url_for('Menu'))
    
    return render_template(
        'menu.html', 
        form_post = form_post, 
        form_escola = form_escola, 
        posts = posts, 
        form_empresa = form_empresa, 
        form_aluno = form_aluno, 
        form_funcionario_escola = form_funcionario_escola, 
        form_funcionario_empresa = form_funcionario_empresa,
        alunos = alunos,
        empresas = empresas,
        escolas = escolas,
        funcionarios_escola = funcionarios_escola,
        funcionarios_empresa = funcionarios_empresa,
        form_vagas = form_vagas,
        vagas_postadas = vagas_postadas
        )

# criando a rota vagas
@app.route('/vagas/', methods=['GET', 'POST'])
@login_required
def Vagas_Page():
    form_vagas = VagasForm()
    
    # O seu processamento de banco de dados (que você comentou que fará depois) entra aqui:
    if form_vagas.validate_on_submit():
        form_vagas.save()
        return redirect(url_for('Vagas_Page'))
        
    return render_template('vagas.html', form_vagas=form_vagas)

# criando a rota projetos
@app.route('/projetos/', methods=['GET', 'POST'])
@login_required
def Projetos_Page():
    
    return f"<h1>Pagina Projetos</h1>"

# criando a rota perfil
@app.route('/perfil/', methods=['GET', 'POST'])
@login_required
def Perfil_Page():
    
    return f"<h1>Pagina Perfil</h1>"

