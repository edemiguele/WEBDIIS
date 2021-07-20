
from .entities.reservas import reservas
from .entities.personas import personas

class modeloReserva():
    @classmethod
    def listar_reservas(self,db, user):
         try:
            print('listar_reservas')
            dir=personas.query.filter_by(usr_danae=user).first()
            print(dir)
            listasReservas=reservas.query.filter_by(correo=dir.correo).all() 
            print(listasReservas) 
            return listasReservas
         except Exception as ex:
            print(ex)
            raise Exception(ex)
           
    
    @classmethod
    def registrar_reservas(self, db, reservas, *args, **kwargs):
        try:
            print(reservas.falta+'--'+reservas.finicio+'--'+reservas.ffin)
            
            db.session.add(reservas)
            db.session.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def eliminar_reserva(self, db, reservas, *args, **kwargs):
        try:
            print(reservas.falta+'--'+reservas.finicio+'--'+reservas.ffin)
            
            db.session.delete(reservas)
            db.session.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
    
