# importando o aplicativo, db (banco)
from sistema import app, db

# importando a função render_template, url_for
from flask import render_template, url_for, request, redirect, flash

# importando as dependencias de login
from flask_login import login_user, logout_user, current_user, login_required

# importando a classe da tabela onde vou salvar
from sistema.models import Usuario

# importando as classes de formulario
from sistema.forms import Geral

# criando uma rota
@app.route('/', methods=["GET", "POST"])
def Menu():

    return render_template('menu.html')