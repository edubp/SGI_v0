from app import db
from datetime import datetime

class Equipamento(db.Model):
    __tablename__ = 'equipamento'

    id = db.Column('id',db.Integer,primary_key = True, autoincrement = True)
    equipamento = db.Column(db.String(100))
    codigo = db.Column(db.String(100), unique=True)
    fabricante = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    serie = db.Column(db.String(100))
    certificado = db.Column(db.String(100), nullable=True)
    periodicidade = db.Column(db.Integer())
    descricao = db.Column(db.Text(),nullable=True)
    data_ultima_calibracao = db.Column(db.DateTime(),nullable=True)
    data_proxima_calibracao = db.Column(db.DateTime(), nullable=True)
    data_registro = db.Column( db.DateTime(),nullable=False,default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'),nullable=True)
    usuario = db.relationship('Usuario', back_populates="equipamentos")

    def __init__(self, equipamento = None, codigo = None, fabricante = None,modelo =None,serie =None, certificado =None,periodicidade =None,descricao =None,data_ultima_calibracao =None, data_proxima_calibracao =None,data_registro =None,usuario_id= None):
        self.equipamento = equipamento
        self.codigo = codigo
        self.fabricante = fabricante
        self.modelo = modelo
        self.serie = serie
        self.certificado = certificado
        self.periodicidade =periodicidade
        self.descricao = descricao
        self.data_ultima_calibracao = data_ultima_calibracao
        self.data_proxima_calibracao = data_proxima_calibracao
        self.data_registro = data_registro
        self.usuario_id = usuario_id

    def __str__(self):
        return self.equipamento