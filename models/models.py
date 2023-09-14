from database import db
from flask_login import UserMixin


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.String(100), nullable=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    funcao = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=False)

    def __init__(self, nome, sobrenome, funcao, email, senha):
        self.nome = nome
        self.sobrenome = sobrenome
        self.funcao = funcao
        self.email = email
        self.senha = senha
        self.active = 1

    def is_active(self):
        return self.active

    def __repr__(self):
        return "Usuario: {}". format(self.nome)
    
class Servico(db.Model): 
    __tablename__ = "servicos"
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(100), nullable=True)
    titulo = db.Column(db.String(100), nullable=False)
    resumo = db.Column(db.String(1000), nullable=False)

class Parceiro(db.Model): 
    __tablename__ = "Parceiros"
    id = db.Column(db.Integer, primary_key=True)
    logomarca = db.Column(db.String(100), nullable=False)

class Portfolio(db.Model): 
    __tablename__ = "Portfolios"
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(100), nullable=False)

class Conteudo(db.Model): 
    __tablename__ = "conteudos"
    id = db.Column(db.Integer, primary_key=True)
    capa = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    resumo = db.Column(db.String(1000), nullable=False)
    conteudo = db.Column(db.String(1000), nullable=False)
    token = db.Column(db.String(20), unique=True, nullable=False)


class Subconteudo(db.Model):
    __tablename__ = "subconteudos"
    id = db.Column(db.Integer, primary_key=True)
    sub_imagem = db.Column(db.String(100), nullable=False)
    sub_titulo = db.Column(db.String(100), nullable=False)
    sub_conteudo = db.Column(db.String(10000), nullable=False)
    token_id = db.Column(db.Integer, db.ForeignKey('conteudos.id'))
    token_relacionado = db.relationship('Conteudo', backref='subconteudos_relacionados', foreign_keys=[token_id], lazy=True)

class Subtopico(db.Model):
    __tablename__ = "subtopicos"
    id = db.Column(db.Integer, primary_key=True)
    subtopico_imagem = db.Column(db.String(100), nullable=False)
    subtopico_conteudo = db.Column(db.String(10000), nullable=False)
    subtopico_id = db.Column(db.Integer, db.ForeignKey('subconteudos.id'))
    subtopico_relacionado = db.relationship('Subconteudo', backref='subtopicos_relacionados', foreign_keys=[subtopico_id], lazy=True)






