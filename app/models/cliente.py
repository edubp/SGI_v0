from app import db
from sqlalchemy.orm import relationship


class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column('id',db.Integer,primary_key = True, autoincrement = True)
    nome = db.Column(db.String(100))
    mci = db.Column(db.String(50), unique=True)
    contato = db.Column(db.String(100),nullable=True)
    telefone1 = db.Column(db.String(100),nullable=True)
    telefone2 = db.Column(db.String(100),nullable=True)
    email1 = db.Column(db.String(100),nullable=True)
    email2 = db.Column(db.String(100),nullable=True)
    razao_social = db.Column(db.String(200),nullable=True)
    endereco = db.Column(db.String(400),nullable=True)
    equipamentos = db.Column(db.Text(),nullable=True)
    agendamento = relationship('Agendamento',back_populates="cliente")


    def __str__(self):
        return self.nome