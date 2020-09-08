from flask import Blueprint, render_template,request,redirect,url_for,send_file
from flask_login import login_required, current_user
from app.models.equipamento import Equipamento
from app.models.usuario import Usuario
from app import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import time
import os

equip = Blueprint('equip', __name__)

@equip.route('/equipamentos')
@login_required
def equipamentos():
    equipamentos = Equipamento.query.all()
    data_hoje = datetime.today()
    return render_template('equipamentos.html',equipamentos = equipamentos,data_hoje=data_hoje, relativedelta=relativedelta)

@equip.route('/adicionarEquipamento', methods = ['GET', 'POST'])
@login_required
def adicionarEquipamento():
    if request.method == 'POST':
        equi = request.form['equipamento']
        codigo = request.form['codigo']
        fabricante = request.form['fabricante']
        modelo = request.form['modelo']
        serie = request.form['serie']
        certificado = request.form['certificado']
        periodicidade = request.form['periodicidade']
        descricao = request.form['descricao']
        try:
            data_ultima_calibracao = datetime.strptime(request.form['data_ultima'],'%Y-%m-%d')
        except:
            data_ultima_calibracao = None
        try:
            data_proxima_calibracao = datetime.strptime(request.form['data_proxima'], '%Y-%m-%d')
        except:
            data_proxima_calibracao = None
        id_usuario = request.form['usuario']
        data_registro = datetime.today()
        usuario = Usuario.query.get(id_usuario)
        # data_registro = request.form['data_registro']

        equipamento = Equipamento(equipamento = equi, codigo=codigo,certificado = certificado,fabricante=fabricante,modelo=modelo,serie=serie,periodicidade=periodicidade,descricao=descricao,data_ultima_calibracao=data_ultima_calibracao,data_proxima_calibracao=data_proxima_calibracao,data_registro=data_registro,usuario=usuario)
        db.session.add(equipamento)
        db.session.commit()
        return redirect(url_for('equip.equipamentos'))

    usuarios = Usuario.query.all()
    return render_template('equipamento.html',usuarios = usuarios)

@equip.route('/editarEquipamento/<int:id>', methods= ['GET', 'POST'])
def editar(id):
    equipamento = Equipamento.query.get(id)
    if request.method == 'POST':
        equipamento.equi = request.form['equipamento']
        equipamento.codigo = request.form['codigo']
        equipamento.fabricante = request.form['fabricante']
        equipamento.modelo = request.form['modelo']
        equipamento.serie = request.form['serie']
        equipamento.certificado = request.form['certificado']
        equipamento.periodicidade = request.form['periodicidade']
        equipamento.descricao = request.form['descricao']
        try:
            equipamento.data_ultima_calibracao = datetime.strptime(request.form['data_ultima'], '%Y-%m-%d')
        except:
            equipamento.data_ultima_calibracao = None
        try:
            equipamento.data_proxima_calibracao = datetime.strptime(request.form['data_proxima'], '%Y-%m-%d')
        except:
            equipamento.data_proxima_calibracao = None
        id_usuario = request.form['usuario']
        equipamento.data_registro = datetime.now()
        equipamento.usuario = Usuario.query.get(id_usuario)
        db.session.commit()
        return redirect(url_for('equip.equipamentos'))

    usuarios = Usuario.query.all()
    try:
        data_ultima = equipamento.data_ultima_calibracao.strftime(("%Y-%m-%d" ))
    except:
        data_ultima = None
    try:
        data_proxima = equipamento.data_proxima_calibracao.strftime(("%Y-%m-%d"))
    except:
        data_proxima = None
    return render_template('editarequipamento.html',e = equipamento, usuarios = usuarios, usuario = equipamento.usuario, data_ultima = data_ultima, data_proxima=data_proxima )

@equip.route('/deletarEquipamento/<int:id>')
def deletar(id):
    equipamento = Equipamento.query.get(id)
    db.session.delete(equipamento)
    db.session.commit()
    return redirect(url_for('equip.equipamentos'))


def verivicar_validade():
    equipamentos = Equipamento.query.all()
    data_hoje = datetime.today()

    for e in equipamentos:
        if e.data_calibracao + relativedelta(years=e.periodicidade)< data_hoje - relativedelta(months=1):
            email = e.usuario.email
            equipamento = e.equipamento
            codigo = e.codigo
            msg = 'Aviso Automático!!!\n\nO equipamento: {} de código : {} está com a calibração vencida!\n\nVerificar Laeta Web!\n\nObrigado!\nAtt, Gestão da Qualidade Laeta.'.format(equipamento,codigo)
            #mandar_email(email,msg)
        elif e.data_calibracao + relativedelta(years=e.periodicidade)< data_hoje:
            email = e.usuario.email
            equipamento = e.equipamento
            codigo = e.codigo
            msg = 'Aviso Automático!!!\n\nO equipamento: {} de código : {} está com a calibração a vencer!\n\nVerificar Laeta Web!\n\nObrigado!\nAtt, Gestão da Qualidade Laeta.'.format(
                equipamento, codigo)
           # mandar_email(email, msg)

@equip.route('/baixar_Lista_Equipamentos/<file>')
def baixarArquivo(file):

    path = os.path.join(os.getcwd(), 'app\static\Excel\Lista_Mestre')

    arquivo = os.path.join(path, file)



    return send_file(arquivo, mimetype='imagem/png')


@equip.route('/download_Equipamentos')
def download_Equipamentos():

    # p = pd.read_sql_query('select * from equipamento',con=db.session.bind)
    # print(p.head())
    # p = pd.read_sql_table('equipamento', con=db.session.bind)
    p = pd.read_sql('equipamento', con=db.session.bind)

    date = datetime.now()
    date = date.strftime("%d_%m_%Y_%H_%M_%S")

    #basedir = os.path.abspath(os.path.dirname(__file__))
    #print(basedir)

    path = os.path.join(os.getcwd(), 'app\static\Excel\Lista_Mestre')

    #arquivo = 'app\static\Excel\lista_mestre{}.xlsx'.format(date)
    arquivo = os.path.join(path,'lista_mestre{}.xlsx'.format(date))


    p.to_excel(arquivo, index=True, header=True)

    # if os.path.isfile(arquivo):
    #     print()
    #     return send_file(arquivo, mimetype='planilha/xlsx')
        # send_file(arquivo, mimetype='planilha/xlsx')


    files = os.listdir(path)
    return render_template('download_lista_mestre.html',files=files)

