import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class  reservas(db.Model):
    __tablename__='reservas'
    idreservas=db.Column(db.Integer(), primary_key=True)
    idespacio=db.Column(db.Integer(), nullable=False)
    correo=db.Column(db.String(150), nullable=False)
    falta=db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now())
    ipalta=db.Column(db.String(45), nullable=False)
    finicio=db.Column(db.DateTime(), nullable=False)
    ffin=db.Column(db.DateTime(), nullable=False)
    observaciones=db.Column(db.String(200))
    
    espacio_id = db.Column(db.String(45), db.ForeignKey("espacios.idespacios"))
    
    nbEspacio = db.relationship("espacios", foreign_keys=[espacio_id])
    # def __str__(self):
    #     return self.idreservas

    # def formatea_falta(self):
    #     return datetime.strftime(self.falta, '%d/%m/%Y - %H:%M:%S')
    
    # def formatea_finicio(self):
    #     return datetime.strftime(self.finicio, '%d/%m/%Y - %H:%M:%S')

    # def formatea_ffin(self):
    #     return datetime.strftime(self.ffin, '%d/%m/%Y - %H:%M:%S')
        
        