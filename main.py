from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_login import logout_user
from models.models import Usuario
from routes.main_routes import main_routes
from routes.main_adm import main_adm
from flask_login import LoginManager, current_user
from flask_mail import Mail
#from flask_jwt_extended import JWTManager, jwt_required
from database import db


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'marcus.s.ribeiro@outlook.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = 'marcus.s.ribeiro@outlook.com'
mail = Mail(app)


app.config['SECRET_KEY'] = 'minha-chave'
app.config['JWT_SECRET_KEY'] = 'super-secret'
#jwt = JWTManager(app)
conexao = "sqlite:///minhadb.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/img/'
app.register_blueprint(main_routes)
app.register_blueprint(main_adm, url_prefix="/staffer")
db.init_app(app)
migracao = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))






if __name__ == "__main__":
    app.run(debug=True, host="192.168.0.111", port="5084")