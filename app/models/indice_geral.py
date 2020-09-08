from app import db
from datetime import  datetime
from enum import Enum

class Indice_Geral(db.Model):

    __tablename__ = 'indice_geral'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    data_realizacao_calibracao = db.Column(db.DateTime(),nullable=True)
    data_registro = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    certificado = db.Column(db.String(50))
    descricao = db.Column(db.Text(), nullable=True)

    agendamento_id = db.Column(db.Integer, db.ForeignKey('agendamento.id'), nullable=True)
    agendamento = db.relationship('Agendamento', back_populates="indice_geral")

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    usuario = db.relationship('Usuario', back_populates="indice_geral")



    def __str__(self):
        return self.processo