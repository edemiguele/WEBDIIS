from app.models.modelo_espacios import modeloEspacios
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import DateField
from datetime import date
from .models.modelo_personas import modeloPersona 
from .models.modelo_reservas import modeloReserva
from .models.modelo_espacios import modeloEspacios
from .models.entities.reservas import reservas
from .models.entities.espacios import espacios
from .common.utilldap import Ldap

from .common.filters import format_datetime
from app.models import modelo_reservas
from sqlalchemy import *
from datetime import datetime

#Conexion con la BBDD *************************************
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'danae03.cps.unizar.es'
app.config['MYSQL_USER'] = 'adminjv'
app.config['MYSQL_PASSWORD'] = 'd1s-aRc'
app.config['MYSQL_DB'] = 'jueves'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminjv:d1s-aRc@danae03.cps.unizar.es:3306/jueves'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#***********************************************************    

db=SQLAlchemy(app)
      
class DateForm(Form):
    dt = DateField('Pick a Date', format="%m/%d/%Y_%H:%M")

app.secret_key = 'SHH!'


@app.route('/')
def index():
    user = request.environ.get("REMOTE_USER")
    return render_template('index.html')

# Cuando no se encuentre la pagina ira a errores/404.html y mostrara el error indicado en esa pagina
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

# http://127.0.0.1:5000/usuarios
@app.route('/usuarios')
def listar_personas():
    try:        
        personas=modeloPersona.listar_personas(db)
        data={
            'personas': personas
        }  
        #llama a listado_personas.html pasandole los datos de la variable data.      
        return render_template('listado_personas.html', data=data)
    except Exception as ex:
        print("Excepcion:" , ex)

# http://127.0.0.1:5000/reservas
@app.route('/reservas', methods=["GET", "POST"])
# Este metodo tiene todas las acciones de los botones de la pagina.
def listar_reservas():
    try:     
        #IMPORTANTE!!!! ******************************
        # cuando se suba al servidor de aplicacion hay que descomentar y comental las variables user e ip porque 
        # en local no funciona porque no hay conexion a ldap para la validacion   
        # user = request.environ.get("REMOTE_USER")
        # ip = request.environ.get("REMOTE_ADDR")

        user = 'eva77'
        ip = '222.222.222.222'

        grupo=Ldap.buscar()

        espacios=modeloEspacios.listar_espacios(db)
        persona=modeloPersona.listar_persona(db, user)
        persona.grupo=grupo

        # Si no hay ninguna persona con el usuario indicado muestra la pagina:
        if not persona:
            return render_template('usuarionoexiste.html')
        else:
            # En el caso de que el metodo que llegue sea un POST (se ha pulsado un boton)
            if request.method == 'POST':
                data3={
                    'espacios': espacios
                }
                # Si ha pulsado el boton Crear
                if request.form.get('crearReserva') == 'Crear':
                    return render_template('nueva_reserva.html', data3=data3)
                # Si ha pulsado el boton Eliminar
                elif  request.form.get('eliminar') == 'eliminar':
                    #print(request.form.get('reserva'))
                    # Si no ha seleccionado ninguna reserva para eliminar
                    if request.form.get('reserva') is None :
                        error='Debe seleccionar una reserva para eliminar'
                        return render_template('errores/error.html', error=error)
                    else :
                        reservas.idreservas=request.form['reserva']
                        data = {}
                        try:
                            data['exito'] = modeloReserva.eliminar_reserva(db, reservas)
                        except Exception as ex:
                            data['mensaje'] = format(ex)
                            data['exito'] = False
                        return jsonify(data)
                # Si ha pulsado el boton Modificar
                elif request.form.get('modificar') == 'modificar':
                    #print('modificar')
                    # Si no ha seleccionado ninguna reserva para modificar
                    if request.form.get('reserva') is None :
                        error='Debe seleccionar una reserva para modificar'
                        return render_template('errores/error.html', error=error)
                    else :
                        reservas.idreservas=request.form['reserva']
                        resul = {}
                        try:                            
                            row = modeloReserva.listar_reserva(db, reservas)
                            resul['exito']=true
                            #print(row[0])
                            #print(dict(row[0]))
                            dicreserva=dict(row[0])
                            
                            reservas.idespacio=dicreserva['idespacio']
                            reservas.correo=dicreserva['correo']
                            reservas.falta=dicreserva['falta']
                            reservas.ipalta=dicreserva['ipalta']
                            reservas.finicio=dicreserva['finicio']
                            reservas.ffin=dicreserva['ffin']
                            reservas.observaciones=dicreserva['observaciones']
                            
                            #print(reservas.observaciones)
                            data={
                                'reserva': reservas            
                            }
                            return render_template('modreserva.html', data3=data3, data=data)
                        except Exception as ex:
                            print(ex)
                            resul['mensaje'] = format(ex)
                            resul['exito'] = False  
                # Si ha pulsado Para Otro para realizar la reserva para otra persona
                elif request.form.get('otro') == 'Para Otro':
                    idpersona = request.form['nbpersona']
                    lreservas=modeloReserva.listar_reservasCorreo(db, idpersona)
                    #lreservas=modeloReserva.todas_reservas(db)
                    persona=modeloPersona.listar_personaCorreo(db, idpersona)
       
                    if not lreservas:
                        data={
                            'reservas': ''            
                        }
                    else:
                        data={
                            'reservas': lreservas            
                        }
                    data2={
                        'personas': persona
                    }
                    data3={
                        'espacios': espacios
                    }
                    form = DateForm()
                    if form.validate_on_submit():
                        return form.dt.data.strftime('%x')
                    #print('data2: ', data2.values)
                    return render_template('listado_reservasOtro.html', data=data, data2=data2, data3=data3, form=form)
            # Listado de todas las reservas
            else:
                lreservas=modeloReserva.listar_reservas(db, user)
                tpersonas=modeloPersona.listar_personas(db)
                if not lreservas:
                    data={
                        'reservas': ''            
                    }
                else:
                    data={
                        'reservas': lreservas            
                    }
                data2={
                    'personas': persona
                }
                data3={
                    'espacios': espacios
                }
                data4={
                    'personas': tpersonas
                }
                form = DateForm()
                if form.validate_on_submit():
                    return form.dt.data.strftime('%x')
                #print('data3: ', data3)
                return render_template('listado_reservas.html', data=data, data2=data2, data3=data3, data4=data4, form=form)
    except Exception as ex:
        print("Excepcion listar reservas:", ex)

# http://127.0.0.1:5000/reservasOtros
@app.route('/reservasOtros', methods=["GET", "POST"])
# Este metodo tiene todas las acciones de los botones de la pagina.
def listar_reservasOtros():
    try:     
        idpersona = request.form['idpersona']
        persona=modeloPersona.listar_personaCorreo(db, idpersona)
        data2={
            'personas': persona
        }
        # En el caso de que el metodo que llegue sea un POST (se ha pulsado un boton)
        espacios=modeloEspacios.listar_espacios(db)
        data3={
            'espacios': espacios
        }
        # Si ha pulsado el boton Crear
        if request.form.get('crearReserva') == 'Crear':
            return render_template('nueva_reservaTodos.html', data3=data3, data2=data2)
            # Si ha pulsado el boton Eliminar
        elif  request.form.get('eliminar') == 'eliminar':
            #print(request.form.get('reserva'))
            # Si no ha seleccionado ninguna reserva para eliminar
            if request.form.get('reserva') is None :
                error='Debe seleccionar una reserva para eliminar'
                return render_template('errores/error.html', error=error)
            else :
                reservas.idreservas=request.form['reserva']
                data = {}
                try:
                    data['exito'] = modeloReserva.eliminar_reserva(db, reservas)
                except Exception as ex:
                    data['mensaje'] = format(ex)
                    data['exito'] = False
                return jsonify(data)
        # Si ha pulsado el boton Modificar
        elif request.form.get('modificar') == 'modificar':
            #print('modificar')
            # Si no ha seleccionado ninguna reserva para modificar
            if request.form.get('reserva') is None :
                error='Debe seleccionar una reserva para modificar'
                return render_template('errores/error.html', error=error)
            else :
                reservas.idreservas=request.form['reserva']
                resul = {}
                try:                            
                    row = modeloReserva.listar_reserva(db, reservas)
                    resul['exito']=true
                    #print(row[0])
                    #print(dict(row[0]))
                    dicreserva=dict(row[0])
                    
                    reservas.idespacio=dicreserva['idespacio']
                    reservas.correo=dicreserva['correo']
                    reservas.falta=dicreserva['falta']
                    reservas.ipalta=dicreserva['ipalta']
                    reservas.finicio=dicreserva['finicio']
                    reservas.ffin=dicreserva['ffin']
                    reservas.observaciones=dicreserva['observaciones']
                    
                    #print(reservas.observaciones)
                    data={
                        'reserva': reservas            
                    }
                    return render_template('modreserva.html', data3=data3, data=data)
                except Exception as ex:
                    print(ex)
                    resul['mensaje'] = format(ex)
                    resul['exito'] = False  
                           
    except Exception as ex:
        print("Excepcion listar reservas:", ex)


@app.route('/nuevaReserva', methods=["GET", "POST"])
def registrar_reservas():
    #IMPORTANTE!!!! ******************************
        # cuando se suba al servidor de aplicacion hay que descomentar y comental las variables user e ip porque 
        # en local no funciona porque no hay conexion a ldap para la validacion   
        # user = request.environ.get("REMOTE_USER")
        # ip = request.environ.get("REMOTE_ADDR")

    user = 'eva77'
    ip='222.222.222.222'
    
    observaciones = request.form['observaciones']
    finicio = request.form['inicio']        
    ffin =  request.form['fin']      
    nbespacios = request.form['nbespacios']
    idespacio=modeloEspacios.listar_espacio(db,nbespacios)
    persona=modeloPersona.listar_persona(db, user)
        
    data = {}
    try:
        reserva = reservas(idespacio=idespacio.idespacios, correo=persona.correo, falta='2021-05-19 14:00:00', ipalta=ip,finicio=finicio, ffin=ffin, observaciones=observaciones)
        data['exito'] = modeloReserva.registrar_reservas(db, reserva)
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)

@app.route('/nuevaReservaOtros', methods=["GET", "POST"])
def registrar_reservasOtro():
    #IMPORTANTE!!!! ******************************
        # cuando se suba al servidor de aplicacion hay que descomentar y comental las variables user e ip porque 
        # en local no funciona porque no hay conexion a ldap para la validacion   
        # user = request.environ.get("REMOTE_USER")
        # ip = request.environ.get("REMOTE_ADDR")
    
    user = 'eva77'
    ip='222.222.222.222'
    
    observaciones = request.form['observaciones']
    finicio = request.form['inicio']                         
    ffin =  request.form['fin'] 
    nbespacios = request.form['nbespacios']
    idespacio=modeloEspacios.listar_espacio(db,nbespacios)
    idpersona = request.form['idpersona']
    
    data = {}
    try:
        reserva = reservas(idespacio=idespacio.idespacios, correo=idpersona, falta='2021-05-19 14:00:00', ipalta=ip,finicio=finicio, ffin=ffin, observaciones=observaciones)
        data['exito'] = modeloReserva.registrar_reservas(db, reserva)
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)

@app.route('/modReserva', methods=["POST"])
def modificar_reserva():
     #IMPORTANTE!!!! ******************************
        # cuando se suba al servidor de aplicacion hay que descomentar y comental las variables user e ip porque 
        # en local no funciona porque no hay conexion a ldap para la validacion   
        # user = request.environ.get("REMOTE_USER")
        # ip = request.environ.get("REMOTE_ADDR")
    
    id=request.form['id']    
    user = 'eva77'
    ip='222.222.222.222'
    
    observaciones = request.form['observaciones']
    data = {}
    try:
        reserva = reservas(idreservas=id, idespacio=null, correo=null, falta=null, ipalta=ip,finicio=null, ffin=null, observaciones=observaciones)
        data['exito'] = modeloReserva.modificar_reserva(db, reserva)
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    if data['exito']==True :
        return redirect(url_for('listar_reservas'))
    else :
        return jsonify(data)

@app.route('/datetimepicker')
def ver_datetimepicker():
    try:
        return render_template('prueba.html')
    except Exception as ex:
        print("Excepcion:"+ex)

@app.route('/calendar')
def ver_calendar():
    try:
        return render_template('prueba2.html')
    except Exception as ex:
        print("Excepcion:",ex)

@app.route('/fichero')
def leer_fichero():
    try:
        return render_template('errores/404.html'), 404
    except Exception as ex:
        print("Excepcion:",ex)

@app.route('/todasreservas', methods=["GET", "POST"])
def todas_reservas():
    try:        
        #IMPORTANTE!!!! ******************************
        # cuando se suba al servidor de aplicacion hay que descomentar y comental las variables user e ip porque 
        # en local no funciona porque no hay conexion a ldap para la validacion   
        # user = request.environ.get("REMOTE_USER")
        # ip = request.environ.get("REMOTE_ADDR")

        user = 'eva77'
        ip = request.environ.get("REMOTE_ADDR")
        
        espacios=modeloEspacios.listar_espacios(db)
        persona=modeloPersona.listar_persona(db, user)

        if not persona:
            return render_template('usuarionoexiste.html')
        else:
            
            lreservas=modeloReserva.todas_reservas(db)
                
            if not lreservas:
                data={
                    'reservas': ''            
                }
            else:
                data={
                    'reservas': lreservas            
                }
            data2={
                'personas': persona
            }
            data3={
                'espacios': espacios
            }
            form = DateForm()
            if form.validate_on_submit():
                return form.dt.data.strftime('%x')
            print('data3: ', data3)
            return render_template('todas_reservas.html', data=data, data2=data2, data3=data3, form=form)
    except Exception as ex:
        print("Excepcion listar reservas:", ex)

def inicializar_app(config):    
    app.config.from_object(config)
    db.init_app(app)
    db.create_all()
    app.register_error_handler(404, pagina_no_encontrada)
    return app

def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime