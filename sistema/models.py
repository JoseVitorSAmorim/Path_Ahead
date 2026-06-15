from sistema import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# criando uma tabela
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(200), nullable=True)
    
    # coloque o resto dos atributos necessario