from .entities.personas import personas

class modeloPersona():
    @classmethod
    def listar_personas(self,db):
        try:                   
            listapersonas=personas.query.all()      
            return listapersonas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def listar_persona(self, db, user):
        try:
            print ('en listar personas')
            dir=personas.query.filter_by(usr_danae=user).first()
            print (dir)
            return dir
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def registrar_persona(self, db, persona):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO personas ( correo, nombre_completo, usr_danae, colectivo, activo) 
                    VALUES (uuid(), '{0}', {1})""".format( persona.correo, persona.nombre_completo, persona.usr_danae, persona.colectivo, persona.activo)
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)