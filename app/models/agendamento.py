from app import db
from datetime import  datetime
from enum import Enum

class Agendamento(db.Model):

    __tablename__ = 'agendamento'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    equipamento = db.Column(db.String(100))
    processo = db.Column(db.String(50))
    prazo = db.Column(db.String(20))
    descricao = db.Column(db.Text(),nullable=True)
    data_calibracao = db.Column(db.DateTime(),nullable=True)
    data_registro = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    laboratorio = db.Column(db.String(100))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    cliente = db.relationship('Cliente',back_populates="agendamento")
    indice_geral = db.relationship('Indice_Geral',back_populates="agendamento")



    def __str__(self):
        return self.processo

    def get_data_evento(self):
        return self.data_calibracao.strftime('%d/%m/%Y')

    def get_cliente(self):
        return self.processo

    def get_evento_atrasado(self):
        if self.data_calibracao < self.datetime.now() - self.timedelta(hours=1):
            return True
        else:
            False


# class UP_UO(Enum):
#     LAB1 = 'LAB1'
#     LAB2 = 'LAB2'
#     LAB3 = 'LAB3'
