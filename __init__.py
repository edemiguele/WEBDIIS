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

from .common.filters import format_datetime
from app.models import modelo_reservas
from sqlalchemy import *
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'danae03.cps.unizar.es'
app.config['MYSQL_USER'] = 'adminjv'
app.config['MYSQL_PASSWORD'] = 'd1s-aRc'
app.config['MYSQL_DB'] = 'jueves'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminjv:d1s-aRc@danae03.cps.unizar.es:3306/jueves'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#db=MySQL(app)
db=SQLAlchemy(app)

class DateForm(Form):
    dt = DateField('Pick a Date', format="%m/%d/%Y_%H:%M")

app.secret_key = 'SHH!'

@app.route('/')
def index():
    user = request.environ.get("REMOTE_USER")
    return render_template('index.html')

def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

@app.route('/usuarios')
def listar_personas():
    try:        
        personas=modeloPersona.listar_personas(db)
        data={
            'personas': personas
        }        
        return render_template('listado_personas.html', data=data)
    except Exception as ex:
        print("Excepcion:" + ex)

@app.route('/reservas', methods=["GET", "POST"])
def listar_reservas():
    try:        
        #user = request.environ.get("REMOTE_USER")
        user = 'eva77'
        print(user)  
        ip = request.environ.get("REMOTE_ADDR")
        print (ip)
        espacios=modeloEspacios.listar_espacios(db)
        persona=modeloPersona.listar_persona(db, user)
        if not persona:
            return render_template('usuarionoexiste.html')
        else:
            if request.method == 'POST':
                observaciones = request.form['observaciones']
                finicio = request.form['inicio']                           
                ffin =  request.form['fin']      
                nbespacios = request.form['nbespacios']
                idespacio=modeloEspacios.listar_espacio(db,nbespacios)
                data = {}
                try:
                    reserva = reservas(idespacio=idespacio.idespacios, correo=persona.correo, falta='2021-05-19 14:00:00', ipalta=ip,finicio=finicio, ffin=ffin, observaciones=observaciones)
                    data['exito'] = modeloReserva.registrar_reservas(db, reserva)
                except Exception as ex:
                    data['mensaje'] = format(ex)
                    data['exito'] = False
                    return jsonify(data)
        
            lreservas=modeloReserva.listar_reservas(db, user)
            if not lreservas:
                print('reserva vacia')
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

            return render_template('listado_reservas.html', data=data, data2=data2, data3=data3, form=form)
    except Exception as ex:
        print("Excepcion:"+ ex)

@app.route('/nuevaReserva', methods=["GET", "POST"])
def registrar_reservas():
    user = request.environ.get("REMOTE_USER")
    ip = request.environ.get("REMOTE_ADDR")
    data = {}                
    try:
        reserva = reservas(idespacio='1', correo='edemiguel@unizar.es', falta='2021-05-19 14:00:00', ipalta=ip,finicio='2021-05-20 09:00:00', ffin='2021-05-20 11:00:00', observaciones='primera reunion')
        data['exito'] = modeloReserva.registrar_reservas(db, reserva)
        
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
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
        print("Excepcion:"+ex)

@app.route('/fichero')
def leer_fichero():
    try:
        return render_template('errores/404.html'), 404
    except Exception as ex:
        print("Excepcion:"+ex)


def inicializar_app(config):    
    app.config.from_object(config)
    db.init_app(app)
    db.create_all()
    app.register_error_handler(404, pagina_no_encontrada)
    return app


def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime