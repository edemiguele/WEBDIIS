from .entities.espacios import espacios

class modeloEspacios():
    @classmethod
    def listar_espacios(self,db):
        try:
            listaespacios=espacios.query.all()  
            return listaespacios
        except Exception as ex:
            print (ex)
            raise Exception(ex)

    @classmethod
    def listar_espacio(self, db, nbespacio):
        try:
            idespacio=espacios.query.filter_by(nbespacios=nbespacio).first()
            return idespacio
        except Exception as ex:
            raise Exception(ex)