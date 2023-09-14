from flask import Flask, Blueprint, request, render_template, url_for, abort, redirect, flash, get_flashed_messages, current_app, session
from flask_login import current_user, login_user, login_required, logout_user
from models.models import Conteudo, Subconteudo, Usuario, Parceiro, Portfolio, Servico
from models.forms import loginForm
from models.forms import postForm
from models.forms import registerForm
from werkzeug.utils import secure_filename
import os
from database import db
import secrets

main_adm = Blueprint('adm', __name__, template_folder='../templates_adm')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""@main_adm.before_request
def check_user_active():
    if not request.path.startswith('/login'):
        if not current_user.is_authenticated or not current_user.active:
            #return 'Unauthorized', 401
            return redirect(url_for('main.index'))"""

@main_adm.before_request
def check_user_active():
    if not current_user.is_authenticated or not current_user.active:
        if request.endpoint and not request.endpoint.startswith('main_adm.login'):
            logout_user()
            session.clear()
            return redirect(url_for('main.index'))



def permissão(permission_level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if user is None or user.get("permission_level", 0) < permission_level:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator




@main_adm.route('/register', methods=["GET", "POST"])
def registrar():
    form = registerForm()
    if request.method == "POST" and form.validate_on_submit():
        dados = Usuario(nome=form.nome.data, sobrenome=form.sobrenome.data, funcao=form.funcao.data, email=form.email.data, senha=form.senha.data)

        db.session.add(dados)
        db.session.commit()
        print('Cadastrado com sucesso:', form.nome.data)
        return redirect(url_for('main.login'))
    else:
        print(form.errors)
    
    return render_template('registrar.html', form=form)

@main_adm.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = registerForm()
    user = Usuario.query.filter_by(id=current_user.id).first()
    query = Usuario.query.order_by(Usuario.id.desc()).all()
    quantidade = Usuario.query.count() 
    posts = Conteudo.query.count() 
    return render_template("dashboard.html", quantidade=quantidade, query=query, posts=posts, form=form, user=user)

@main_adm.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return "Usuário não encontrado."

    if request.method == 'POST':
        data = request.get_json()
        active = data.get('active', False)  # Valor default é False caso não seja enviado

        usuario.active = active
        db.session.commit()
        return "Dados atualizados com sucesso!" 

@main_adm.route("/criar_posts", methods=["GET", "POST"])
def criar():
    user = Usuario.query.filter_by(id=current_user.id).first()
    return render_template("criar_post.html", user=user)

@main_adm.route('/upload', methods=['POST'])
def upload_file():
    capa = request.files['capa']
    sub_imagens = request.files.getlist('sub_imagem')  # Usamos getlist para recuperar várias imagens
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
    resumo = request.form['resumo']
    sub_titulo = request.form.getlist('sub_titulo')
    sub_conteudo = request.form.getlist('sub_conteudo')
    token = generate_token()

    if capa and allowed_file(capa.filename):
        filename = secure_filename(capa.filename)
        capa.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        caminho_imagem = os.path.join('/', current_app.config['UPLOAD_FOLDER'], filename)

        conteudo = Conteudo(capa=caminho_imagem, titulo=titulo,conteudo=conteudo, resumo=resumo, token=token)
        db.session.add(conteudo)
        db.session.commit()

        for st, sc, si in zip(sub_titulo, sub_conteudo, sub_imagens):
            if si and allowed_file(si.filename):
                filename = secure_filename(si.filename)
                si.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                caminho_imagem = os.path.join('/', current_app.config['UPLOAD_FOLDER'], filename)

                sub_conteudo = Subconteudo(sub_imagem=caminho_imagem, sub_titulo=st, sub_conteudo=sc, token_relacionado=conteudo)
                db.session.add(sub_conteudo)
            else:
                return "Erro: Uma das sub-imagens é um arquivo inválido."

        db.session.commit()
        return 'Dados inseridos com sucesso!'
    else:
        return "Erro: A capa é um arquivo inválido."
def generate_token():
    return secrets.token_urlsafe(20)

@main_adm.route("/criar_parceiros", methods=["GET", "POST"])
@login_required
def criar_parceiros():
    user = Usuario.query.filter_by(id=current_user.id).first()
    return render_template("parceiros.html", user=user)

@main_adm.route('/upload_parceiros', methods=['POST'])
@login_required
def upload_parceiros():
    logomarca = request.files['logomarca']
    if logomarca and allowed_file(logomarca.filename):
        filename = secure_filename(logomarca.filename)
        logomarca.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        caminho_imagem = os.path.join('/', current_app.config['UPLOAD_FOLDER'], filename)

        parceiro = Parceiro(logomarca=caminho_imagem)
        db.session.add(parceiro)
        db.session.commit()

        return "Upload bem-sucedido!"  # Adicionando um retorno após o upload bem-sucedido
    else:
        return "Erro: A capa é um arquivo inválido."
    

@main_adm.route("/criar_portfolio", methods=["GET", "POST"])
@login_required
def criar_portfolio():
    user = Usuario.query.filter_by(id=current_user.id).first()
    return render_template("criar_portfolio.html", user=user)

@main_adm.route('/upload_portfolio', methods=['POST'])
@login_required
def upload_portfolio():
    portfolio = request.files['portfolio']
    if portfolio and allowed_file(portfolio.filename):
        filename = secure_filename(portfolio.filename)
        portfolio.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        caminho_imagem = os.path.join('/', current_app.config['UPLOAD_FOLDER'], filename)

        portfolio = Portfolio(imagem=caminho_imagem)
        db.session.add(portfolio)
        db.session.commit()

        return "Upload bem-sucedido!"  # Adicionando um retorno após o upload bem-sucedido
    else:
        return "Erro: A capa é um arquivo inválido."
    
@main_adm.route("/criar_consultorias", methods=["GET", "POST"])
@login_required
def criar_consultoria():
    user = Usuario.query.filter_by(id=current_user.id).first()
    return render_template("criar_consultoria.html", user=user)

@main_adm.route('/upload_consultoria', methods=['POST'])
@login_required
def upload_consultoria():
    imagem = request.files['imagem']
    titulo = request.form['titulo']
    resumo = request.form['resumo']
    if imagem and allowed_file(imagem.filename):
        filename = secure_filename(imagem.filename)
        imagem.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        caminho_imagem = os.path.join('/', current_app.config['UPLOAD_FOLDER'], filename)

        servico = Servico(imagem=caminho_imagem, titulo=titulo, resumo=resumo)
        db.session.add(servico)
        db.session.commit()

        return "Upload bem-sucedido!"
    elif not imagem:
        caminho_imagem = None

        servico = Servico(imagem=caminho_imagem, titulo=titulo, resumo=resumo)
        db.session.add(servico)
        db.session.commit()

        return "Upload bem-sucedido! (Sem imagem)"
    else:
        return "Erro: A capa é um arquivo inválido."
    



@main_adm.route("/editar_slides", methods=["GET", "POST"])
def editar_slides():
    user = Usuario.query.filter_by(id=current_user.id).first()

    return render_template("editar_slides.html", user=user)

@main_adm.route('/editar_post/<int:id>', methods=['GET', 'POST'])
def editar_post(id):
    conteudo = Conteudo.query.get(id)
    if request.method == 'POST':
        conteudo.titulo = request.form['titulo']
        db.session.commit()  # Salvar as alterações no banco de dados
        return redirect(url_for('adm.lista_publicacao'))
    return render_template('editar.html', conteudo=conteudo)

@main_adm.route('/deletar/<int:id>', methods=["GET", "POST"])
@login_required
def delete(id):
    delete = Conteudo.query.get(id)

    if request.method == "POST":
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for('adm.lista_publicacao', delete=delete))
        print(db.session.delete(delete))
    return redirect(url_for('adm.lista_publicacao'))


@main_adm.route('/logout')
@login_required
def logout():
  logout_user()
  session.clear()
  return redirect(url_for('main.index'))

@main_adm.route("/visualizar_pagina")
@login_required
def visualizar_pagina():
    query = Conteudo.query.order_by(Conteudo.id.desc()).all()
    logomarca = Parceiro.query.order_by(Parceiro.id.desc()).all()
    portfolio = Portfolio.query.order_by(Portfolio.id.desc()).all()
    servico = Servico.query.order_by(Servico.id.desc()).all()
    return render_template("index_adm.html", query=query, logomarca=logomarca, portfolio=portfolio, servico=servico )



    
@main_adm.route("/lista_publicacoes")
@login_required
def lista_publicacao():
    user = Usuario.query.filter_by(id=current_user.id).first()
    query = Usuario.query.order_by(Usuario.id.desc()).all()
    quantidade = Usuario.query.count() 
    post = Conteudo.query.order_by(Conteudo.id.desc()).all()
    return render_template("lista_publicacoes.html", quantidade=quantidade, query=query, post=post, user=user)


    



