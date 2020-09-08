from flask import Blueprint, render_template,request,redirect,url_for, send_file
from flask_login import login_required, current_user
import calendar
from datetime import  datetime,date
from app.models.cliente import Cliente
from app.models.agendamento import Agendamento
from app import db
from sqlalchemy import extract
import os
import pandas as pd

agendamento = Blueprint('agendamento', __name__)
calendario = calendar.Calendar()

@agendamento.route('/agendamentos', methods = ['GET','POST'])
@login_required
def agendamentos():

    matriz = []
    if request.method == 'POST':
        mes = int(request.form['mes'])
        ano = int(request.form['ano'])
        laboratorio = request.form['laboratorio']

        lista = processarCalendario(mes, ano, laboratorio)

        return render_template('agendamentos.html', c=lista, ano=str(ano), mes=str(mes), laboratorio = laboratorio)

    mes = datetime.now().month
    ano = datetime.now().year
    laboratorio='Laboratório 1 : Thiago / Mauro'
    lista = processarCalendario(mes,ano,laboratorio)
    return render_template('agendamentos.html',c=lista, ano = str(ano) , mes =str(mes),laboratorio = laboratorio )

@agendamento.route('/listarTodosAgendamentos')
@login_required
def listarTodosAgendamentos():
    agendamentos = Agendamento.query.all()

    return render_template('listar_todos_agendamentos.html', agendamentos = agendamentos)


@agendamento.route('/fazerAgendamento/<dia>/<mes>/<ano>')
@agendamento.route('/fazerAgendamento',methods = ['POST'])
@login_required
def fazerAgendamento(dia = None, mes = None, ano = None):

    if request.method =='POST':
        equipamento = request.form['equipamento']
        prazo = request.form['prazo']
        processo = request.form['processo']
        descricao = request.form['descricao']
        data_calibracao = datetime.strptime(request.form['data_calibracao'],'%Y-%m-%d')
        data_registro = datetime.today()
        laboratorio = request.form['laboratorio']
        id_cliente = request.form['cliente']
        cliente = Cliente.query.get(id_cliente)

        agendamento = Agendamento(equipamento=equipamento,prazo = prazo, processo = processo,  descricao = descricao, data_calibracao = data_calibracao, data_registro = data_registro, laboratorio = laboratorio, cliente = cliente)
        db.session.add(agendamento)
        db.session.commit()
        return redirect(url_for('agendamento.agendamentos'))
    data  = datetime(int(ano), int(mes), int(dia))
    clientes = Cliente.query.all()
    return render_template('fazerAgendamento.html', clientes=clientes, data = data)


@agendamento.route('/listaAgendamentoPorData/<dia>/<mes>/<ano>')
@login_required
def listaAgendamentoPorData(dia = None, mes = None, ano = None):
    d = date(int(ano), int(mes), int(dia))

    agendamentos = Agendamento.query.filter(extract('month', Agendamento.data_calibracao) == str(mes),extract('day', Agendamento.data_calibracao) == str(dia),extract('year', Agendamento.data_calibracao) == str(ano)).all()

    return render_template('lista_agendamento_por_data.html', agendamentos = agendamentos)

@agendamento.route('/editarAgendamento/<int:id>', methods= ['GET', 'POST'])
def editar(id):
    agendamento = Agendamento.query.get(id)

    if request.method == 'POST':

        try:
            agendamento.data_calibracao = datetime.strptime(request.form['data_calibracao'], '%Y-%m-%d')
        except:
            agendamento.data_calibracao = None

        agendamento.processo = request.form['processo']
        agendamento.equipamento = request.form['equipamento']
        agendamento.prazo = request.form['prazo']
        agendamento.laboratorio = request.form['laboratorio']
        agendamento.cliente = request.form['cliente']
        agendamento.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('agendamento.agendamentos'))

    try:
        data = agendamento.data_calibracao.strftime(("%Y-%m-%d"))
    except:
        print('erro da função editar agendamento.py')
        data = None
    clientes = Cliente.query.all()
    return render_template('editarAgendamento.html', c = agendamento, data = data,cliente = agendamento.cliente, clientes = clientes)

@agendamento.route('/deletarAgendamento/<int:id>')
def deletar(id):
    agendamento = Agendamento.query.get(id)
    db.session.delete(agendamento)
    db.session.commit()
    return redirect(url_for('agendamento.listarTodosAgendamentos'))



def processarCalendario(mes,ano,laboratorio):
    lista = []
    dia_da_semana=''

    agendamentos = Agendamento.query.filter(extract('month', Agendamento.data_calibracao) == str(mes), Agendamento.laboratorio == laboratorio).all()
    for i in calendario.monthdatescalendar(ano, mes):
        for i in i:
            if i.month != mes:
                pass
            else:
                if i.weekday() == 0:
                    dia_da_semana = 'Segunda'
                elif i.weekday() == 1:
                    dia_da_semana = 'Terça'
                elif i.weekday() == 2:
                    dia_da_semana = 'Quarta'
                elif i.weekday() == 3:
                    dia_da_semana = 'Quinta'
                elif i.weekday() == 4:
                    dia_da_semana = 'Sexta'
                elif i.weekday() == 5:
                    dia_da_semana = 'Sábado'
                elif i.weekday() == 6:
                    dia_da_semana = 'Domingo'

                if agendamentos != []:

                    lista_agendamento = [agenda for agenda in agendamentos if i.day == agenda.data_calibracao.day and i.month == agenda.data_calibracao.month ]
                    for j in range(4):
                        try:
                            x =  lista_agendamento[j]
                        except:
                            lista_agendamento.append('-----------')

                    lista.append((i.day, i.month, i.year, dia_da_semana, lista_agendamento))
                    lista_agendamento=[]

                else:
                    lista_agendamento = ['-----------','-----------','-----------','-----------']
                    lista.append((i.day, i.month, i.year, dia_da_semana, lista_agendamento))



    return lista

@agendamento.route('/baixar_Agendamentos/<file>')
def baixarArquivo(file):

    path = os.path.join(os.getcwd(), 'app\static\Excel\Agendamentos')

    arquivo = os.path.join(path, file)



    return send_file(arquivo, mimetype='imagem/png')


@agendamento.route('/download_Agendamentos')
def download_Agendamentos():

    # p = pd.read_sql_query('select * from equipamento',con=db.session.bind)
    # print(p.head())
    # p = pd.read_sql_table('equipamento', con=db.session.bind)
    p = pd.read_sql('agendamento', con=db.session.bind)

    date = datetime.now()
    date = date.strftime("%d_%m_%Y_%H_%M_%S")

    #basedir = os.path.abspath(os.path.dirname(__file__))
    #print(basedir)

    path = os.path.join(os.getcwd(), 'app\static\Excel\Agendamentos')

    #arquivo = 'app\static\Excel\lista_mestre{}.xlsx'.format(date)
    arquivo = os.path.join(path,'agendamentos{}.xlsx'.format(date))


    p.to_excel(arquivo, index=True, header=True)

    # if os.path.isfile(arquivo):
    #     print()
    #     return send_file(arquivo, mimetype='planilha/xlsx')
        # send_file(arquivo, mimetype='planilha/xlsx')


    files = os.listdir(path)
    return render_template('download_lista_mestre.html',files=files)

