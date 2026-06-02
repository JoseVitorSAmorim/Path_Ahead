# EPT-Trabalho
O nome poderá mudar posteriormente

# Conteudo
trabalho feito para o desafio EPT, aqui a ideia e assimilar a relação de modo mais pratico entre escolas, empresas e alunos. Ajudando todos de uma só vez.

# Problematica
A maioria dos alunos que estão saindo do ensino medio tem dificuldade para entrar no mercado de trabalho, e o nosso cenario é para o pessoal da tecnologia e ensino tecnico, oque vizamos melhor a correspondencia de vaga, armazenando algumas informações em seus perfis, tendo em vista a falta de experiencia profissional.

# Resolução
Criamos a ideia, e nesse momento eu criei o mvp incompleto por incrivel que pareça da ideia, com uma abordagem mais explicativa de como as coisas vao funcionar, pois a "IA" não conseguiu escrever direito o front-end com as configurações do meu sistema, então falta algumas inserções e adendos, porém já está funcionando por enquanto.

# Como usar
Crie a pasta virtual:
    -> python -m venv venv

Instale o req:
    -> pip install -r requirements.txt

*Se necessario*

Crie o banco de dados:
    -> flask db init
    -> flask db migrate -m "migração de teste e avaliação"
    -> flask db upgrade

Rode o arquivo:
    -> no terminal, app.py
    -> se necessario python app.py
    -> acessar o link gerado

# Utilizando
Crie um Admin e faça testes, pois ainda n foi verificado o tipo de usuario nas paginas, e estou com um problema na correlação de acessos, então por agora esse sistema está dependente de um usuario com a categoria "Admin".