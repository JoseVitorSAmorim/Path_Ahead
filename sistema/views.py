# importando o aplicativo, db (banco)
from sistema import app, db

# importando a função render_template, url_for
from flask import render_template, url_for, request, redirect, flash

# importando as dependencias de login
from flask_login import login_user, logout_user, current_user, login_required

# importando a classe da tabela onde vou salvar
from sistema.models import Usuario, Aluno, Empresa, Escola, Funcionario

# importando as classes de formulario
from sistema.forms import CadastroForm, LoginForm, AlunoForm, EscolaForm, EmpresaForm, FuncionarioForm

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

# criando o Menu
@app.route('/menu-feed', methods=['GET', 'POST'])
def Menu():
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
    
    # validando os formularios

    ### Formulario empresa ###
    if 'btn_empresa' in request.form:
        if form_empresa.validate_on_submit():
            form_empresa.save(current_user.id)

            return redirect(url_for('Menu'))
    
    ### Formulario escola ###
    if 'btn_escola' in request.form:
        if form_escola.validate_on_submit():
            form_escola.save(current_user.id)

            return redirect(url_for('Menu'))
        
    ### Formulario aluno ###
    if 'btn_aluno' in request.form:
        if form_aluno.validate_on_submit():
            form_aluno.save(current_user.id)

            return redirect(url_for('Menu'))
        
    ### Formulario funcionario ###
    if 'btn_funcionario' in request.form:
        if form_funcionario.validate_on_submit():
            form_funcionario.save(current_user.id)

            return redirect(url_for('Menu'))
    
    return render_template('menu.html', form_aluno=form_aluno, form_empresa=form_empresa, form_escola=form_escola, form_funcionario=form_funcionario)