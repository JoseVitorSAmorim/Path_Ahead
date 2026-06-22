# Path ahead - Em desenvolvimento
> [!NOTE]
> Trata-se de uma MVP e não de um produto pronto.

## Objetivo
Uma plataforma, no estilo de rede social, onde Colégios estaduais paranaenses e Empresas poderão interagir de forma eficiente e prático
## Público-alvo
### Estudante
Para o estudante, poderá postar evento, condecoração ou projeto que está envolvido; e inscrever-se em vagas de trabalho ou serviço.
### Empresa
Para a Empresa, a partir de seus funcionários cadastrados na plataforma, poderá abrir vagas de trabalho ou de serviço(freelance); vizualizar posts no feed.
### Colégio
Para o Colégio, a partir de seus professores e pedagogos/coordenadores cadastrados na plataforma, poderá postar evento, condecoração ou projeto que está envolvido; e indicar estudantes em vagas de trabalho.
## Tecnologias usadas
- HTMX e Tailwind CSS
- Django
- PostgreSQL
- Docker
---
# Parte legal
## Trademarks and Usage Policy

The name **Path ahead**, along with its logos, visual identity, branding designs, and associated assets, are the exclusive property of **José Vitor Santana de Amorim**.

The source code license applied to this repository (Apache License 2.0) grants you permissions to use, modify, and distribute the software code, but **DOES NOT grant** any rights, licenses, or permissions to use our trademarks, trade names, or logos.

If you modify, fork, or redistribute this software for commercial or public use, you are expressly required to:
1. Remove all original logos, proprietary visual assets, and direct name references to our brand.
2. Rename the project so that it does not cause user confusion and does not imply any endorsement, sponsorship, or official affiliation with our team.
---
# Área de desenvolvimento
> [!IMPORTANT]
> Para criar feature, antes crie uma branch com o nome develop/nome_da_feature.

> [!WARNING]
> Antes de integrar a feature na main, teste na branch test.

## Preparando o ambiente
### Linux
```
sudo apt update
sudo apt install -y git python3.12 python3.12-venv python3-pip libpq-dev gcc
sudo apt install -y docker-compose-v2
```
### Windows
- Baixe e instale o Python 3.12 pelo site oficial (marque a opção "Add python.exe to PATH" no instalador).
- Baixe, instale e inicialize o Docker Desktop. Certifique-se de ativar a integração com o WSL2 se solicitado.

## Ativando o ambiente
### Linux
```
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
### Windows
```
python -m venv .venv
.\\.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## Validando o Docker
- Subir os containers pela primeira vez
```
docker compose up --build
```
- Rodar as migrações iniciais
```
docker compose exec web python manage.py migrate
```
- Criar um superusuário para acessar o painel administrativo
```
docker compose exec web python manage.py createsuperuser
```
## Configurando o .env
> [!CAUTION]
> Nunca suba senhas para o GitHub. todo arquivo secreto que contenha credencias, sempre escreva o nome do arquivo no .gitignore para não subir

Crie um arquivo chamado .env na raiz do projeto e adicione as configurações do banco de dados:
```
DEBUG=True
SECRET_KEY=sua-chave-secreta-do-django
POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario_db
POSTGRES_PASSWORD=senha_db
```

## Tratamento de Erro
### Permission denied ao rodar Docker no Linux
- Causa: O seu usuário não está no grupo do docker.
- Solução: Rode o comando, feche o terminal, faça Logoff no sistema operacional e abra novamente.
```
sudo usermod -aG docker $USER
```
### Port 5432 is already in use
- Causa: Você possui um PostgreSQL instalado nativamente na sua máquina física competindo com o Docker.
- Solução: Pare o serviço local antes de subir o docker.
  - Linux:
```
sudo systemctl stop postgresql
```
  - Windows:
    - Abra o app Serviços (services.msc), localize postgresql, clique com o botão direito e selecione Parar.
### O script do Windows fecha sozinho ou dá erro de política
- Causa: O Windows bloqueia a execução de scripts baixados da internet ou criados localmente por segurança.
- Solução: Solução: Certifique-se de abrir o PowerShell como Administrador e digitar Set-ExecutionPolicy RemoteSigned -Scope Process antes de chamar o script .\\setup.ps1.
