from app import app, db, lm
from flask import render_template,flash, redirect, url_for, Blueprint
from flask_login import login_user , logout_user, login_required, login_manager,current_user
from app.models.usuario import Usuario

main = Blueprint('main', __name__)

@main.route("/")
def index():
    if current_user.is_authenticated:
        return render_template('index_main.html', name=current_user.nome)
    return redirect(url_for('auth.login'))


@lm.user_loader
def load_user(user_id):
# since the user_id is just the primary key of our user table, use it in the query for the user
    return Usuario.query.get(int(user_id))
