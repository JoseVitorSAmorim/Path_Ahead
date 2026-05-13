# importando o aplicativo
from sistema import app, db

if __name__ == "__main__": # aqui fala "se a chamada for desse arquivo, ele vai rodar o app." 
    with app.app_context():
        db.create_all() # criar as tabelas antes do site toda vez que rodar o app, evitar erros
    app.run(debug=True) # nao recomendado pois pode rodar em um lugar errado, o debug diz que toda vez que fizer uma alteração no codigo, o site vai atualizar tambem