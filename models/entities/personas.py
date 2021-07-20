from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class personas(db.Model):
    __tablename__='personas'
    correo=db.Column(db.String(150), primary_key=True)
    nombre_completo=db.Column(db.String(150), nullable=False)
    usr_danae=db.Column(db.String(25), nullable=False)
    colectivo=db.Column(db.String(3), nullable=False)
    activo=db.Column(db.Integer(), nullable=False)
    
    def __str__(self):
        return self.correo    

    
        