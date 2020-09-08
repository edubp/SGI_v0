from app import app, db, lm
from flask import render_template,flash, redirect, url_for, Blueprint
from flask_login import login_user , logout_user, login_required, login_manager,current_user
from app.models.usuario import Usuario

laeta = Blueprint('laeta', __name__)

@laeta.route("/index")
def index():
    if current_user.is_authenticated:
        return render_template('index_laeta.html', name=current_user.nome)
    return redirect(url_for('auth.login'))


@laeta.route("/colaboradores")
def colaboradores():
    if current_user.is_authenticated:
        return render_template('colaboradores_laeta.html', name=current_user.nome)
    return redirect(url_for('auth.login'))