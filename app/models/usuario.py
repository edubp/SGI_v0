from app import db
from flask_login import UserMixin
from enum import Enum
from sqlalchemy.orm import relationship

class Usuario (UserMixin,db.Model):
    __tablename__ = 'usuario'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    up_uo = db.Column(db.String(50))
    privilegio = db.Column(db.String(50))
    matricula = db.Column(db.String(50))
    ramal = db.Column(db.String(50))
    equipamentos = relationship("Equipamento", back_populates="usuario")
    indice_geral = db.relationship('Indice_Geral', back_populates="usuario")

    def __init(self,email,nome,up_uo,privilegio,senha):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.up_uo = up_uo
        self.privilegio = privilegio

    def __repr__(self):
        return "<User %r>" % self.nome

class UP_UO(Enum):
    DIMCI = 'DIMCI'
    DIAVI = 'DIAVI'
    LAETA = 'LAETA'
    LAENA = 'LAENA'
    LAVIB = 'LAVIB'
    LABUS = 'LABUS'
