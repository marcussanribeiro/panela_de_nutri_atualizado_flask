from flask import Flask, Blueprint, request, render_template, url_for, abort, redirect, flash, get_flashed_messages
from flask_login import current_user, login_user, login_required
from models.forms import loginForm
from models.models import Conteudo, Subconteudo, Subtopico, Usuario, Parceiro, Portfolio, Servico
from flask_mail import Message
from database import db
import secrets

main_routes = Blueprint('main', __name__, template_folder='../templates_geral')


@main_routes.route("/")
def index():
    query = Conteudo.query.order_by(Conteudo.id.desc()).all()
    logomarca = Parceiro.query.order_by(Parceiro.id.desc()).all()
    portfolio = Portfolio.query.order_by(Portfolio.id.desc()).all()
    servico = Servico.query.order_by(Servico.id.desc()).all()
    return render_template("index.html", query=query, logomarca=logomarca, portfolio=portfolio, servico=servico )

@main_routes.route('/posts/<token>')
def show_post(token):
    post = Conteudo.query.filter_by(token=token).first()
    if not post:
        return 'Post não encontrado!'

    subconteudos = Subconteudo.query.filter_by(token_id=post.id).all()
    subconteudo_ids = [subconteudo.id for subconteudo in subconteudos]  # Lista de IDs dos subconteúdos
    subtopicos = Subtopico.query.filter(Subtopico.subtopico_id.in_(subconteudo_ids)).all()
    

    return render_template('post.html', post=post, subconteudos=subconteudos, subtopicos=subtopicos)

def generate_token():
    return secrets.token_urlsafe(20)

@main_routes.route('/formulario_enviado')
def formulario_enviado():
    return 'Dúvida enviada com sucesso! Em breve entraremos em contato.'

@main_routes.route('/processar_formulario', methods=['POST'])
def processar_formulario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    mensagem = request.form.get('mensagem')

    from main import mail  # Importe aqui para evitar a circular import

    msg = Message('Nova dúvida do formulário de contato',
                  recipients=['tickets@odygamers.p.tawk.email'])
    msg.body = f'Nome: {nome}\nE-mail: {email}\nMensagem: {mensagem}'

    mail.send(msg)

    return redirect(url_for('main.formulario_enviado'))



@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if current_user.is_authenticated:
        return redirect(url_for('adm.dashboard'))
    else:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            senha = form.senha.data
            user = Usuario.query.filter_by(email=email).first()
            #if not user.email or senha:
                #flash('O email ou a senha não estão corretos', 'error')
            if user and (user.email != email or user.senha != senha or user.active == 0):
                flash('O email ou a senha não estão corretos', 'error')
            if user and user.email == email and user.senha == senha and user.active == 1:
                login_user(user)
                return redirect(url_for('adm.dashboard'))

        messages = get_flashed_messages()
    return render_template('login.html', form=form, messages=messages)

