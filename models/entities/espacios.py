from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
class espacios(db.Model):
    __tablename__='espacios'
    idespacios=db.Column(db.Integer(), primary_key=True)
    nbespacios=db.Column(db.String(45), nullable=False)
    idtipoespacio=db.Column(db.Integer(), nullable=False)

    def __str__(self):
        return self.nbespacio    
        