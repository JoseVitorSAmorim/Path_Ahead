# importando o aplicativo, db (banco)
from sistema import app, db

# importando a função render_template, url_for
from flask import render_template, url_for, request, redirect, flash

# importando as dependencias de login
from flask_login import login_user, logout_user, current_user, login_required

# importando a classe da tabela onde vou salvar
from sistema.models import Usuario

# importando as classes de formulario
from sistema.forms import LoginForm, CadastroForm

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
def Logout():
    logout_user()
    
    return redirect(url_for('Login'))

# criando a rota menu
@app.route('/menu/', methods=['GET', 'POST'])
def Menu():

    return render_template('menu.html')