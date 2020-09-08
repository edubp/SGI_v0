from flask import Blueprint, render_template,request,redirect,url_for,send_file
from flask_login import login_required, current_user
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app import db
import os
import pandas as pd
from datetime import datetime

cliente = Blueprint('cliente', __name__)

@cliente.route('/clientes')
@login_required
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html',clientes = clientes)

@cliente.route('/adicionarCliente', methods = ['GET', 'POST'])
@login_required
def adicionarCliente():
    if request.method == 'POST':
        nome = request.form['nome']
        mci = request.form['mci']
        contato = request.form['contato']
        telefone1 = request.form['telefone1']
        telefone2 = request.form['telefone2']
        email1 = request.form['email1']
        email2 = request.form['email2']
        razao_social = request.form['razao_social']
        endereco = request.form['endereco']
        equipamentos = request.form['equipamentos']

        cliente = Cliente(nome = nome, mci = mci , contato = contato , telefone1 = telefone1, telefone2 = telefone2, email1 = email1, email2 = email2, razao_social = razao_social, endereco = endereco, equipamentos = equipamentos)
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('cliente.clientes'))

    return render_template('cliente.html')

@cliente.route('/editarCliente/<int:id>', methods= ['GET', 'POST'])
def editar(id):
    cliente = Cliente.query.get(id)
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.mci = request.form['mci']
        cliente.contato = request.form['contato']
        cliente.telefone1 = request.form['telefone1']
        cliente.telefone2 = request.form['telefone2']
        cliente.email1 = request.form['email1']
        cliente.email2 = request.form['email2']
        cliente.razao_social = request.form['razao_social']
        cliente.endereco = request.form['endereco']
        cliente.equipamentos = request.form['equipamentos']
        db.session.commit()
        return redirect(url_for('cliente.clientes'))

    return render_template('editarCliente.html', c = cliente)

@cliente.route('/deletarCliente/<int:id>')
def deletar(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('cliente.clientes'))

@cliente.route('/baixar_Lista_Clientes/<file>')
def baixarArquivo(file):

    path = os.path.join(os.getcwd(), 'app\static\Excel\Clientes')

    arquivo = os.path.join(path, file)



    return send_file(arquivo, mimetype='imagem/png')


@cliente.route('/download_Clientes')
def download_Clientes():

    # p = pd.read_sql_query('select * from equipamento',con=db.session.bind)
    # print(p.head())
    # p = pd.read_sql_table('equipamento', con=db.session.bind)
    p = pd.read_sql('cliente', con=db.session.bind)

    date = datetime.now()
    date = date.strftime("%d_%m_%Y_%H_%M_%S")

    #basedir = os.path.abspath(os.path.dirname(__file__))
    #print(basedir)

    path = os.path.join(os.getcwd(), 'app\static\Excel\Clientes')

    #arquivo = 'app\static\Excel\lista_mestre{}.xlsx'.format(date)
    arquivo = os.path.join(path,'clientes{}.xlsx'.format(date))


    p.to_excel(arquivo, index=True, header=True)

    # if os.path.isfile(arquivo):
    #     print()
    #     return send_file(arquivo, mimetype='planilha/xlsx')
        # send_file(arquivo, mimetype='planilha/xlsx')


    files = os.listdir(path)
    return render_template('download_lista_clientes.html',files=files)

