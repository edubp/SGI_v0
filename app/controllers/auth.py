from flask import Blueprint , render_template, request,redirect, url_for,flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.usuario import UP_UO,Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    senha = request.form.get('senha')

    remember = True if request.form.get('remember') else False

    user = Usuario.query.filter_by(email=email).first()


    if not user or not check_password_hash(user.senha, senha):
        flash('->')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/registro')
def registro():
    lista_up_uo = []
    for i in UP_UO:
        lista_up_uo.append(str(i)[6:])
    return render_template('Registro.html', lista = lista_up_uo)

@auth.route('/registro', methods=['POST'])
def registro_post():
    email = request.form.get('email')
    nome = request.form.get('nome')
    up_uo = request.form.get('up_uo')
    senha = request.form.get('senha')
    confirmar_senha = request.form.get('confirmar_senha')
    privilegio = 'admin'

    user = Usuario.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in database
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Já existe esse email cadastrado!')
        return redirect(url_for('auth.registro'))
    elif senha != confirmar_senha:
        flash('Senhas não correspondem!')
        return redirect(url_for('auth.registro'))

    print(email, senha,nome)
    novo_usuario = Usuario(email=email, nome=nome, up_uo = up_uo, privilegio =privilegio, senha=generate_password_hash(senha, method='sha256'))

    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))