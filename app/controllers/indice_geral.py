from flask import Blueprint, render_template,request,redirect,url_for,send_file
from flask_login import login_required, current_user
import calendar
from datetime import  datetime,date
from app.models.cliente import Cliente
from app.models.agendamento import Agendamento
from app.models.indice_geral import Indice_Geral
from app.models.usuario import Usuario
from app import db
import os
import pandas as pd

indice = Blueprint('indice', __name__)
calendario = calendar.Calendar()

@indice.route('/indice_geral', methods = ['GET', 'POST'])
@login_required
def indice_geral():

    indice = Indice_Geral.query.all()

    print('INDICE',indice[0].usuario)
    print(indice)

    if request.method == 'POST':
        return render_template('indice_geral.html')

    return render_template('indice_geral.html', indice=indice)


@indice.route('/cadastrarIndice/<id>')
@indice.route('/cadastrarIndice', methods = ['POST'])
@login_required
def cadastrarIndice(id = None):
    agendamento = Agendamento.query.get(id)

    data_realizacao_calibracao= None
    if request.method =='POST':
        try:
            data_realizacao_calibracao = datetime.strptime(request.form['data_realizacao_calibracao'], '%Y-%m-%d')
        except:
            print('erro da função cadastrar indice_geral.py')

        usuario_id = request.form['usuario']
        usuario = Usuario.query.get(usuario_id)
        agendamento_id = request.form['agendamento']
        agendamento = Agendamento.query.get(agendamento_id)
        certificado = request.form['certificado']
        descricao = request.form['descricao']

        indice = Indice_Geral(data_realizacao_calibracao = data_realizacao_calibracao,certificado=certificado,agendamento=agendamento,descricao = descricao, usuario = usuario)

        db.session.add(indice)
        db.session.commit()



        return redirect(url_for('indice.indice_geral'))

    agendamento = Agendamento.query.get(id)
    usuarios = Usuario.query.all()

    return render_template('cadastrar_indice_geral.html',agendamento = agendamento, usuarios = usuarios)



@indice.route('/visualizarIndice/<int:id>')
def editar(id):
    indice = Indice_Geral.query.get(id)
    data_realizacao,data_agendamento = None,None
    try:
        data_realizacao = indice.data_realizacao_calibracao.strftime(("%Y-%m-%d"))
        data_agendamento = indice.agendamento.data_calibracao.strftime(("%Y-%m-%d"))
    except:
        print('erro da função editar agendamento.py')
        data = None

    return render_template('visualizar_indice_geral.html',i = indice,data_agendamento = data_agendamento, data_realizacao = data_realizacao)


@indice.route('/deletarIndice/<int:id>')
def deletar(id):
    indice = Indice_Geral.query.get(id)
    db.session.delete(indice)
    db.session.commit()
    return redirect(url_for('indice_geral'))


@indice.route('/baixar_Lista_Indice_Geral/<file>')
def baixarArquivo(file):

    path = os.path.join(os.getcwd(), 'app\static\Excel\Indice_Geral')

    arquivo = os.path.join(path, file)



    return send_file(arquivo, mimetype='imagem/png')


@indice.route('/download_Indice_Geral')
def download_Indice_Geral():

    # p = pd.read_sql_query('select * from equipamento',con=db.session.bind)
    # print(p.head())
    # p = pd.read_sql_table('equipamento', con=db.session.bind)
    p = pd.read_sql('indice_geral', con=db.session.bind)

    date = datetime.now()
    date = date.strftime("%d_%m_%Y_%H_%M_%S")

    #basedir = os.path.abspath(os.path.dirname(__file__))
    #print(basedir)

    path = os.path.join(os.getcwd(), 'app\static\Excel\Indice_Geral')

    #arquivo = 'app\static\Excel\lista_mestre{}.xlsx'.format(date)
    arquivo = os.path.join(path,'indice_geral{}.xlsx'.format(date))


    p.to_excel(arquivo, index=True, header=True)

    # if os.path.isfile(arquivo):
    #     print()
    #     return send_file(arquivo, mimetype='planilha/xlsx')
        # send_file(arquivo, mimetype='planilha/xlsx')


    files = os.listdir(path)
    return render_template('download_indice_geral.html',files=files)


