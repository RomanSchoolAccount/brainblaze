import io 
from functools import wraps
from flask import app, current_app, jsonify, render_template, send_file, request, redirect, session, flash, url_for
from flask_mail import Message
from db import db, mail
from models import Imagem, User, Produto, Categoria, Favorito, Encomenda
from datetime import datetime, timedelta

CATEGORIAS_FIXAS = {
    1: "Performance mental",
    2: "Energia máxima",
    3: "Alta produtividade",
    4: "Foco extremo",
    5: "Aprendizado rápido",
    6: "Disciplina mental",
    7: "Alta performance"
}

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Precisa de fazer login primeiro!")
            return redirect("/Login")

        if session["username"].lower() != "admin":
            flash("Acesso negado! Esta área é exclusiva para administradores.")
            return redirect("/")
            
        return f(*args, **kwargs)
    return decorated_function


def register_routes(app):
    @app.route("/")
    def home():
        return render_template("index.html")
    
    @app.route('/toggle_favorito/<int:produto_id>', methods=['POST'])
    def toggle_favorito(produto_id):
        if 'user_id' not in session:
            return jsonify({'status': 'login_required'}), 401
        
        user_id = session['user_id']
    
        fav = Favorito.query.filter_by(user_id=user_id, produto_id=produto_id).first()
        
        if fav:
            db.session.delete(fav)
            db.session.commit()
            return jsonify({'status': 'removed'})
        else:
            novo_fav = Favorito(user_id=user_id, produto_id=produto_id)
            db.session.add(novo_fav)
            db.session.commit()
            return jsonify({'status': 'added'})

    @app.route('/Perfil')
    def Perfil():
        if 'user_id' not in session:
            return redirect(url_for('Login'))
            
        user_id = session['user_id']
        username = session.get('username', 'Utilizador')

        favoritos = db.session.query(Produto).join(Favorito).filter(Favorito.user_id == user_id).all()

        compras = Encomenda.query.filter_by(
            cliente=username, 
            estado="Concluída"
        ).all()

        return render_template(
            'UserService.html', 
            username=username, 
            favoritos=favoritos, 
            compras=compras
        )

    @app.route("/Logout")
    def Logout():
        session.clear()
        flash("Sessão terminada com sucesso.")
        return redirect("/")

    @app.route("/adicionar_carrinho/<int:produto_id>", methods=["POST"])
    def adicionar_carrinho(produto_id):
        if "carrinho" not in session:
            session["carrinho"] = []

        carrinho = session["carrinho"]
        carrinho.append(produto_id)
        session["carrinho"] = carrinho

        return redirect("/Carrinho")
    
    @app.route("/Carrinho")
    def Carrinho():
        ids = session.get("carrinho", [])
        produtos = Produto.query.filter(
            Produto.id.in_(ids)
        ).all() if ids else []

        subtotal = sum(produto.preco for produto in produtos)

        if produtos:
            envio = 0.00 if subtotal >= 50.00 else 4.90  
        else:
            envio = 0.00

        total = subtotal + envio

        return render_template(
            "Carrinho.html",
            produtos=produtos,
            subtotal=subtotal,
            envio=envio,
            total=total
        )

    @app.route("/TermosEservicos")
    def TermosEservicos():
        return render_template("TermosEservicos.html")
    
    @app.route("/LivroReclamacoes")
    def LivroReclamacoes():
        return render_template("LivroReclamacoes.html")
    
    @app.route("/PoliticaPrivacidade")
    def PoliticaPrivacidade():
        return render_template("PoliticaPrivacidade.html")

    @app.route("/Recovery", methods=["GET", "POST"])
    def Recovery():
        if request.method == "POST":
            recovery_input = request.form.get("recovery_input")

            user = User.query.filter((User.username == recovery_input) | (User.email == recovery_input)).first()
            
            if user:
                try:
                    msg = Message(
                        subject="Recuperação de Palavra-Passe - BrainBlaze",
                        sender=current_app.config['MAIL_USERNAME'],
                        recipients=[user.email]
                    )

                    msg.body = f"Olá {user.username},\n\nRecebemos um pedido para recuperar a tua conta na BrainBlaze.\nA tua palavra-passe atual é: {user.password}\n\nSe não foste tu a pedir isto, ignora este e-mail.\n\nCumprimentos,\nEquipa BrainBlaze"
                    
                    mail.send(msg)
                    flash("E-mail de recuperação enviado com sucesso! Verifica a tua caixa de entrada.")
                    return redirect("/Login")
                    
                except Exception as e:
                    flash("Erro ao enviar o e-mail. Tenta novamente mais tarde.")
                    return redirect("/Recovery")
            else:
                flash("Não encontrámos nenhuma conta com esse Username ou Email.")
                return redirect("/Recovery")

        return render_template("AccountRecovery.html")

    @app.route("/Novidades")
    def Novidades():
        return render_template("Novidades.html")

    @app.route('/exibir_imagem/<int:id_imagem>')
    def exibir_imagem(id_imagem):
        imagem_db = Imagem.query.get_or_404(id_imagem)
        if not imagem_db.dados:
            return "Imagem não encontrada", 404
            
        return send_file(
            io.BytesIO(imagem_db.dados),
            mimetype='image/jpeg' 
        )


    @app.route("/Achivements")
    def Achivements():
        return render_template("Achivements.html")

    @app.route("/SobreNos")
    def SobreNos():
        return render_template("SobreNos.html")


    @app.route('/Contactos', methods=['GET', 'POST'])
    def Contactos():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            mensagem = request.form.get('mensagem')

            try:
                msg = Message(
                    subject=f"Suporte BrainBlaze - Mensagem de {username}",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=['BrainBlazeshop@gmail.com']
                )
                msg.body = f"Username: {username}\nEmail do Utilizador: {email}\n\nMensagem:\n{mensagem}"
                mail.send(msg)

                return render_template('Contactos.html', success="Mensagem enviada com sucesso!")
            except Exception as e:
                print(f"Erro ao enviar: {e}")
                return render_template('Contactos.html', error="Erro ao enviar a mensagem.")
                
        return render_template('Contactos.html')
    
    @app.route("/Registo", methods=["GET", "POST"])
    def Registo():

        data_limite = (datetime.now() - timedelta(days=16*365.25)).strftime('%Y-%m-%d')

        if request.method == "POST":
            email = request.form.get("email")
            username = request.form.get("username")
            data_nascimento = request.form.get("data_nascimento")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if password != confirm_password:
                flash("As palavras-passe não coincidem!")
                return redirect("/Registo")

            email_exists = User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first() if hasattr(User, 'username') else User.query.filter_by(nome=username).first()

            if email_exists or username_exists:
                flash("O Username ou Email já se encontram registados.")
                return redirect("/Registo")

            campos_user = {
                "email": email,
                "data_nascimento": data_nascimento,
                "password": password
            }
            if hasattr(User, 'username'):
                campos_user["username"] = username
            else:
                campos_user["nome"] = username

            novo_user = User(**campos_user)

            try:
                db.session.add(novo_user)
                db.session.commit()
                flash("Conta criada com sucesso! Faça login.")
                return redirect("/Login")
            except Exception as e:
                db.session.rollback()
                flash("Ocorreu um erro ao criar a conta. Tente novamente.")
                return redirect("/Registo")
            
        
    
        if request.method == 'POST':
                data_nasc_str = request.form.get('data_nascimento')
                if data_nasc_str:
                    data_nasc = datetime.strptime(data_nasc_str, '%Y-%m-%d')
                    idade = (datetime.now() - data_nasc).days // 365.25
                    
                    if idade < 16:
                        flash('Tens de ter pelo menos 16 anos para te registares!', 'error')

        return render_template("Registo.html", data_limite=data_limite)

    @app.route("/Login", methods=["GET", "POST"])
    def Login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if hasattr(User, 'username'):
                user = User.query.filter_by(username=username).first()
            else:
                user = User.query.filter_by(nome=username).first()

            if user and user.password == password:
                session["user_id"] = user.id
                session["username"] = getattr(user, 'username', getattr(user, 'nome', 'Utilizador'))
                
                if session["username"].lower() == "admin":
                    return redirect("/Panel")
                
                return redirect("/")
            else:
                flash("Username ou Palavra-passe incorretos!")
                return redirect("/Login")

        return render_template("Login.html")

    @app.route("/Panel")
    @admin_required
    def Panel():
        from sqlalchemy import func

        total_users = User.query.count()
        total_produtos = Produto.query.count()
        total_categorias = Categoria.query.count()
        total_encomendas = Encomenda.query.count()

        faturacao_hoje = db.session.query(func.sum(Encomenda.total)).scalar() or 0.0
        vendas_semanais = db.session.query(func.sum(Encomenda.total)).scalar() or 0.0

        clientes_recentes = User.query.order_by(User.id.desc()).limit(4).all()

        alertas_stock = Produto.query.filter(Produto.stock < 3).count()

        ultimas_encomendas = Encomenda.query.order_by(Encomenda.id.desc()).limit(5).all()

        return render_template(
            "paneladmin.html",
            total_users=total_users,
            total_produtos=total_produtos,
            total_categorias=total_categorias,
            total_encomendas=total_encomendas,
            clientes_recentes=clientes_recentes,
            faturacao_hoje=faturacao_hoje,
            vendas_semanais=vendas_semanais,
            alertas_stock=alertas_stock,
            ultimas_encomendas=ultimas_encomendas
        )


    @app.route("/Produtos")
    def Produtos():
        lista_produtos = Produto.query.all()
        return render_template("Produtos.html", produtos=lista_produtos, categorias=CATEGORIAS_FIXAS)


    @app.route("/Panel/Produtos")
    @admin_required
    def AdminProdutos():
        lista_produtos = Produto.query.all()

        return render_template("admin_produtos.html", produtos=lista_produtos, categorias=CATEGORIAS_FIXAS)


    @app.route("/Panel/Produtos/Novo", methods=["GET", "POST"])
    @admin_required
    def NovoProduto():
        if request.method == "POST":
            nome = request.form.get("nome")
            descricao = request.form.get("descricao")
            preco = float(request.form.get("preco", 0))
            stock = int(request.form.get("stock", 0))
            categoria_id = request.form.get("categoria_id")

            file = request.files.get("imagem")
            imagem_id = None
            if file and file.filename != '':
                nova_img = Imagem(dados=file.read())
                db.session.add(nova_img)
                db.session.commit()
                imagem_id = nova_img.id

            novo_prod = Produto(
                nome=nome,
                descricao=descricao,
                preco=preco,
                stock=stock,
                desconto=0,
                categoria_id=int(categoria_id) if categoria_id else None,
                imagem_id=imagem_id
            )
            db.session.add(novo_prod)
            db.session.commit()
            return redirect("/Panel/Produtos")

        return render_template("novo_produto.html", categorias=CATEGORIAS_FIXAS)


    @app.route("/Panel/Produtos/Editar/<int:produto_id>", methods=["POST"])
    @admin_required
    def EditarProduto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        produto.nome = request.form.get("nome")
        produto.stock = int(request.form.get("stock"))
        
        cat_id = request.form.get("categoria_id")
        produto.categoria_id = int(cat_id) if cat_id else None
        
        produto.preco = float(request.form.get("preco"))
        
        desconto_input = request.form.get("desconto")
        produto.desconto = int(desconto_input) if (desconto_input and desconto_input.isdigit()) else 0


        file = request.files.get("nova_imagem")
        if file and file.filename != '':
            if produto.imagem_id:
                img_existente = Imagem.query.get(produto.imagem_id)
                if img_existente: img_existente.dados = file.read()
            else:
                nova_img = Imagem(dados=file.read())
                db.session.add(nova_img)
                db.session.commit()
                produto.imagem_id = nova_img.id

        db.session.commit()
        return redirect("/Panel/Produtos")

    @app.route("/Panel/Produtos/Eliminar/<int:produto_id>", methods=["POST"])
    @admin_required
    def EliminarProduto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        db.session.delete(produto)
        db.session.commit()
        return redirect("/Panel/Produtos")


    @app.route("/Panel/Users")
    @admin_required
    def PanelUsers():
        users = User.query.all()
        return render_template("admin_users.html", users=users)

    @app.route("/Panel/Users/Editar/<int:user_id>", methods=["POST"])
    @admin_required
    def EditarUser(user_id):
        user = User.query.get_or_404(user_id)

        user.email = request.form.get("email")
        if request.form.get("password"):
            user.password = request.form.get("password")


        db.session.commit()
        flash(f"Utilizador {user.username} atualizado com sucesso!")
        return redirect("/Panel/Users")

    @app.route("/Panel/Users/Eliminar/<int:user_id>", methods=["POST"])
    @admin_required
    def EliminarUser(user_id):
        user = User.query.get_or_404(user_id)

        if user.username.lower() == "admin":
            flash("Não é possível eliminar o administrador principal!")
            return redirect("/Panel/Users")
            
        db.session.delete(user)
        db.session.commit()
        flash("Utilizador removido com sucesso.")
        return redirect("/Panel/Users")

    
    @app.route("/Panel/Encomendas")
    @admin_required
    def PanelEncomendas():
        encomendas = Encomenda.query.all()
        return render_template(
            "admin_encomendas.html",
            encomendas=encomendas
        )
    
    @app.route('/admin/encomenda/<int:encomenda_id>/concluir', methods=['GET', 'POST'])
    def concluir_encomenda(encomenda_id):
        encomenda = Encomenda.query.get_or_404(encomenda_id)
        
        try:
            encomenda.estado = "Concluída"
            db.session.commit()
            flash(f'Encomenda #{encomenda_id} marcada como concluída com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar o estado da encomenda.', 'error')

        return redirect(url_for('PanelEncomendas'))
    
    @app.route('/checkout', methods=['POST'])
    def checkout():
        if 'user_id' not in session:
            flash('Precisa de fazer login para finalizar a compra.', 'error')
            return redirect(url_for('Login'))

        ids = session.get('carrinho', [])
        if not ids:
            flash('O seu carrinho está vazio!', 'warning')
            return redirect(url_for('Carrinho'))

        produtos = Produto.query.filter(Produto.id.in_(ids)).all()

        subtotal = sum(produto.preco for produto in produtos)
        envio = 0.00 if subtotal >= 50.00 else 4.90
        total_encomenda = subtotal + envio
        
        try:
            nova_encomenda = Encomenda(
                cliente=session.get('username'),
                total=total_encomenda,
                estado="Pendente", 
                data=datetime.utcnow()  
            )

            db.session.add(nova_encomenda)
            db.session.commit()

            session.pop('carrinho', None)

            return render_template('checkout_sucesso.html', total=total_encomenda, encomenda_id=nova_encomenda.id)
            
        except Exception as e:
            db.session.rollback()
            flash('Ocorreu um erro ao processar a encomenda. Tente novamente.', 'error')
            return redirect(url_for('Carrinho'))
        
    @app.route("/remover_carrinho/<int:produto_id>", methods=["POST"])
    def remover_carrinho(produto_id):
        carrinho = session.get("carrinho", [])

        if produto_id in carrinho:
                carrinho.remove(produto_id)
                session["carrinho"] = carrinho
                session.modified = True
                flash("Produto removido com sucesso!", "success")
                
        return redirect(url_for("Carrinho"))
    
    @app.context_processor
    def injetar_dados_globais():
        if 'user_id' in session:
            user_id = session['user_id']
            username = session.get('username')

            favoritos = db.session.query(Produto).join(Favorito).filter(Favorito.user_id == user_id).all()

            compras = Encomenda.query.filter_by(cliente=username, estado="Concluída").all()
            
            return dict(global_favoritos=favoritos, compras=compras)
            
        return dict(global_favoritos=[], compras=[])


    @app.route("/Newsletter", methods=["POST"])
    def newsletter():
        dados = request.get_json()
        email = dados.get("email") if dados else None
            
        if not email:
            return jsonify({"status": "error", "message": "Email inválido!"}), 400
                
            
        print(f"Novo subscritor da newsletter: {email}")
            
        return jsonify({"status": "success", "message": "Obrigado por te registares na nossa Newsletter!"})