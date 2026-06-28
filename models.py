from datetime import datetime

from db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    data_nascimento = db.Column(db.String(50))


class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dados = db.Column(db.LargeBinary, nullable=False)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    descricao = db.Column(db.Text)

    preco = db.Column(db.Float, nullable=False)
    
    desconto = db.Column(db.Integer, default=0)

    stock = db.Column(db.Integer, default=0)

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categoria.id")
    )

    imagem_id = db.Column(
        db.Integer,
        db.ForeignKey("imagem.id")
    )

class Favorito(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)




class Encomenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100))
    total = db.Column(db.Float)
    estado = db.Column(db.String(50), default="Pendente")
    data = db.Column(db.DateTime, default=datetime.utcnow)