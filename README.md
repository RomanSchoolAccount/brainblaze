======================================================================
                    BRAINBLAZE - PLATAFORMA E-COMMERCE
======================================================================

Este projeto consiste numa plataforma de comércio eletrónico (E-Commerce)
desenvolvida em Python utilizando o framework Flask.

A aplicação permite aos utilizadores visualizar produtos, adicionar ao
carrinho, efetuar encomendas e possui uma área de administração para
gestão dos produtos.

======================================================================
1. TECNOLOGIAS UTILIZADAS
======================================================================

• Python 3.11
• Flask 3.x
• Flask-SQLAlchemy
• SQLite
• HTML5
• CSS3
• JavaScript

======================================================================
2. REQUISITOS
======================================================================

Para executar o projeto é necessário ter instalado:

- Python 3.10 ou superior
- pip
- Navegador Web
- (Opcional) Visual Studio Code

Verificar a versão instalada:

python --version

======================================================================
3. ESTRUTURA DO PROJETO
======================================================================

207_FLASK/
│
├── static/
│   ├── Img/
│   ├── JS/
│   │   └── script.js
│   ├── style.css
│   └── favicon.ico
│
├── templates/
│   ├── index.html
│   ├── Produtos.html
│   ├── Carrinho.html
│   ├── Login.html
│   ├── Registo.html
│   ├── admin_produtos.html
│   ├── admin_users.html
│   ├── admin_encomendas.html
│   ├── checkout_sucesso.html
│   └── restantes páginas HTML
│
├── instance/
│   └── database.db
│
├── db.py
├── models.py
├── views.py
├── main.py
└── README.txt

======================================================================
4. INSTALAÇÃO
======================================================================

1. Abrir o terminal na pasta do projeto.

2. Criar um ambiente virtual (recomendado):

Windows:
    python -m venv venv

Linux/macOS:
    python3 -m venv venv

3. Ativar o ambiente virtual.

Windows CMD:
    venv\Scripts\activate

PowerShell:
    .\venv\Scripts\Activate.ps1

Linux/macOS:
    source venv/bin/activate

======================================================================
5. INSTALAR AS DEPENDÊNCIAS
======================================================================

Caso exista um ficheiro requirements.txt:

    pip install -r requirements.txt

Caso contrário:

    pip install Flask
    pip install Flask-SQLAlchemy

======================================================================
6. EXECUTAR O PROJETO
======================================================================

Na pasta principal executar:

    python main.py

ou

    python3 main.py

Depois abrir no navegador:

http://127.0.0.1:5000

======================================================================
7. BASE DE DADOS
======================================================================

A aplicação utiliza SQLite.

O ficheiro da base de dados encontra-se em:

instance/database.db

Caso seja eliminado, poderá ser novamente criado pela aplicação
(consoante a implementação).

======================================================================
8. FUNCIONALIDADES
======================================================================

✔ Registo de utilizadores

✔ Login

✔ Catálogo de produtos

✔ Pesquisa de produtos

✔ Carrinho de compras

✔ Checkout

✔ Área de administração

✔ Gestão de produtos

✔ Gestão de utilizadores

✔ Gestão de encomendas

✔ Página de contactos

✔ Livro de reclamações

======================================================================
9. DEPENDÊNCIAS UTILIZADAS
======================================================================

blinker==1.9.0
click==8.3.1
colorama==0.4.6
Flask==3.1.3
Flask-Mail==0.10.0
Flask-SQLAlchemy==3.1.1
greenlet==3.5.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
PyMySQL==1.2.0
SQLAlchemy==2.0.50
typing_extensions==4.15.0
Werkzeug==3.1.6


======================================================================
10. PROBLEMAS FREQUENTES
======================================================================

Erro:
ModuleNotFoundError

Solução:

Instalar novamente as bibliotecas:

pip install Flask Flask-SQLAlchemy

----------------------------------------------------

Erro:
Address already in use

Solução:

Fechar o servidor Flask anterior ou alterar a porta.

----------------------------------------------------

Erro:
Página sem estilos CSS

Solução:

Limpar a cache do navegador (Ctrl + F5).

======================================================================
11. OBSERVAÇÕES
======================================================================

- As imagens encontram-se na pasta static/Img.

- Os ficheiros JavaScript encontram-se em static/JS.

- As páginas HTML encontram-se em templates/.

- A aplicação segue a arquitetura Flask com separação entre
  modelos, vistas e ficheiro principal.

======================================================================
12. AUTORES
======================================================================

Projeto desenvolvido para a unidade curricular de
Desenvolvimento Web.

Autor(es):

- Roman Carlous Kulachkiskyy
- 224227

======================================================================
