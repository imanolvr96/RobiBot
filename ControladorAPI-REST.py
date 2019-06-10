#------------------------------------------------------------------------------
#               Created by: IMANOL VILLALBA
#               On: 10/06/2019
#------------------------------------------------------------------------------

#! / usr / bin / python3
# - * - codificación: utf-8 - * -

#   --- IMPORTS    ------------------------------------------------------------
import requests, os, pymysql, time, mysql, json
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, make_response, jsonify
from datetime import datetime
from flask_cors import CORS

#   --- I MAKE THE DATA BASE CONECTION    -------------------------------------
try:
    #   opens the database connection
    conexion_db = pymysql.connect("localhost", "admin", "123456", "barberia_bd")

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")

    else:
        conexion_db.close()

#   --- MAKE DE APP WITH FLASK AND CORS  --------------------------------------
#   I create flask application
app = Flask(__name__)

#   I convert flask application to cors application
CORS(app)

#   --- GETING AND SENDING RESPONSE TO DIALOGFLOW -----------------------------
@app.route('/webhook', methods=['POST'])
def webhook():

    #   Getting json of dialogflow
    req = request.get_json(silent = True, force = True)

    #   Setting request to processrequest
    res = processRequest(req)

    #   Setting json witch request to dialogflow
    return make_response(jsonify({'fulfillmentText': res["speech"]}))

#   --- PROCESSING THE REQUEST FROM DIALOGFLOW  -------------------------------
def processRequest(req):

    #   I get and compare the name of the intent
    result = req.get("queryResult")
    intento = result.get("intent")
    displayName = intento.get("displayName")

    #   If the intent is of the climate
    if displayName == "IntentoClima":

        #   I get the parameters
        result = req.get("queryResult")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")

        #   I make the query and I make the json
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=b05fca8f43c5de742a23418eb47e6797&units=metric'.format(city)
        peticionURL = requests.get(url)
        esquemaJSON = peticionURL.json()

        #   Save data that I am interested from the json
        temperatura = str(esquemaJSON['main']['temp'])
        velocidadViento = str(esquemaJSON['wind']['speed'])
        latitud = str(esquemaJSON['coord']['lat'])
        longitud = str(esquemaJSON['coord']['lon'])

        #   I make the string
        speech = "En " + city + " con coordenadas, " + latitud + ", " + longitud + ", hay " + temperatura + "ºC. Con una velocidad del viento de " + velocidadViento + "km/h"

        #   I return speech
        return {
            "speech": speech
                }

    #   If the intent is of the hairdresser
    elif displayName == "IntentoCitaPeluqueria":

        #   I get the parameters
        result = req.get("queryResult")
        parameters = result.get("parameters")
        horaOriginal = parameters.get("time")
        fechaOriginal = parameters.get("date")
        telefono = parameters.get("phone-number")

        #   Cutting the date and time string
        hora = horaOriginal[11:19]
        fecha = fechaOriginal[0:10]

        #   Check if the date and time is past
        if ComrobarFechaHoraActual(fecha, hora):

            #   Check the opening hours
            if ComprobarHorario(hora):

                #   Check if there is any match
                if ComprobarCita(fecha, hora):

                    #   I make the string
                    speech = "Lo siento, ya hay una cita a esa hora"

                    #   I return speech
                    return {
                        "speech": speech
                        }
                else:
                    #   I save the data in the database
                    MySQL(fecha, hora, telefono)

                    #   I make the string
                    str1 = "Correcto! Tienes la cita el "
                    str2 = " a las  "
                    str3 = ". Tu teléfono de contacto es:  "

                    speech = str1 + fecha + str2 + hora + str3 + telefono

                    #   I return speech
                    return {
                        "speech": speech
                        }
            else:
                #   I make the string
                str1 = "Lo siento, esa hora está fuera de nuestro horario. "
                str2 = "Recuerda, para pedir cita de 10:00 a 13:30 o de 16:00 a 19:30."
                str3 = " Solo a en punto o a y media. Gracias!"

                speech = str1 + str2 + str3

                #   I return speech
                return {
                    "speech": speech
                        }
        else:
            #   I make the string
            speech = "Es imposible darte una fecha y hora del pasado"

            #   I return speech
            return {
                "speech": speech
                    }

#   --- CHECK THE OPENING HOURS -----------------------------------------------
def ComprobarHorario(horaCita):

    try:
        #   I create the cursor
        cursorComprobarHorario = conexion_db.cursor()

        #   I execute the query
        cursorComprobarHorario.execute("SELECT horas FROM horario")

        #   Save all cursor results
        resultado = cursorComprobarHorario.fetchall()

        #   I go through the results looking for some coincidence
        for hora in resultado:
            if horaCita in str(hora[0]):
                return True

        #   I close the cursor
        cursorComprobarHorario.close()

    except mysql.connector.Error as err:
        print("Error executing query")
        print(err)

#   --- MYSQL CONEXION  -------------------------------------------------------
def MySQL(fecha, hora, telefono):

    try:
          #   I create the cursor
        cursorMySQL = conexion_db.cursor()

        #   I execute the query
        query = "INSERT INTO `cita` (`fecha`,`hora`,`telefono`) VALUES (%s,%s,%s)"
        insert_tuple = (fecha, hora, telefono)
        cursorMySQL.execute(query, insert_tuple)

        #   I save the data in the database
        conexion_db.commit()

        #   I show the information messages
        print("Registro insertado exitosamente en la tabla cita")
        print(cursorMySQL.rowcount, "registro insertado.")

        #   I close the cursor
        cursorMySQL.close()

    except mysql.connector.Error as err:
        print("Error executing query:")
        print(err)

#   --- CHECK IF THERE IS ANY MACH  -------------------------------------------
def ComprobarCita(fecha, hora):

    try:
        #   I create the cursor
        cursorComprobarCita = conexion_db.cursor()

        #   I execute the query
        cursorComprobarCita.execute("SELECT fecha, hora FROM cita;")

        #   Save all cursor results
        resultado = cursorComprobarCita.fetchall()

        #   I search if coincide the date and time of a reservation
        for horaFecha in resultado:
            if fecha == str(horaFecha[0]) and hora == (str(horaFecha[1])):
                return True

        #   I close the cursor
        cursorComprobarCita.close()

    except mysql.connector.Error as err:
        print("Error executing query")
        print(err)

#   --- CHEK CURRENT DATE AND TIME  -------------------------------------------
def ComrobarFechaHoraActual(fecha, hora):

    #   I save the current date and time
    hora_actual = time.strftime('%H:%M:%S')
    fecha_actual = time.strftime('%Y-%m-%d')

    #   I chek current time and date
    if fecha_actual < fecha:
        return True
    
    elif fecha_actual == fecha:

        if hora_actual < hora:
            return True

        else:
            return False
            
    else:
        return False

#   --- I SHOW THE HOURS IN ANGULAR  ----------------------------------------
@app.route('/horarios',  methods=['get'])
def SelectAngular():
    
    try:
        #   I create the cursor
        cursorSelectAngular = conexion_db.cursor()

        #   I execute the query
        cursorSelectAngular.execute("SELECT id_horario, CONVERT(horas, char), plazas FROM horario;")

        #   Save all cursor results
        resultado = cursorSelectAngular.fetchall()

        #   Change tuple to list to can modify it
        listaUno = list(resultado)

        #   I close the cursor
        cursorSelectAngular.close()

        #   Return the list converted to json
        return json.dumps(parsearListaHorario(listaUno))
        
    except mysql.connector.Error as err:
        print("Error executing query")
        print(err)

#   --- PARSE THE LIST ------------------------------------------------------- 
def parsearListaHorario(miLista):

    #   I make new list and dictionary
    diccionario = []
    lista = []

    #   I pass a list to a dictionary and create a list of dictionaries
    for i in miLista:

        diccionario = {'id': i[0], 'horas': i[1], 'plazas': i[2]}
        
        lista.append(diccionario)

    return lista

#   --- I SHOW THE RESERVATION IN ANGULAR  ------------------------------------
@app.route('/citas',  methods=['get'])
def SelectAngularCitas():

    try:
        #   I create the cursor
        cursorSelectAngularCitas = conexion_db.cursor()

        #   I execute the query
        cursorSelectAngularCitas.execute("SELECT id_cita, CONVERT(fecha, char), CONVERT(hora, char), telefono FROM barberia_bd.cita;")

        #   Save all cursor results
        resultado = cursorSelectAngularCitas.fetchall()

        #   Change tuple to list to can modify it
        listaUno = list(resultado)

        #   I close the cursor
        cursorSelectAngularCitas.close()
        
        #   Return the list converted to json
        return json.dumps(parsearListaCitas(listaUno))

    except mysql.connector.Error as err:
        print("Error executing query")
        print(err)

#   --- PARSE THE LIST --------------------------------------------------------
def parsearListaCitas(miLista):

    #   I make new list and dictionary
    diccionario = []
    lista = []

    #   I pass a list to a dictionary and create a list of dictionaries
    for i in miLista:

        diccionario = {'id': i[0], 'fecha': i[1], 'hora': i[2], 'telefono': i[3]}
        
        lista.append(diccionario)

    return lista

#   --- I DELETE RESERVATION FROM ANGULAR  ------------------------------------
@app.route('/deleteR/<id>',  methods=['delete'])
def DeleteFromAngular(id):

    try:
        #   I create the cursor
        cursorDeleteAngular = conexion_db.cursor()

        #   I execute the query
        cursorDeleteAngular.execute("DELETE FROM cita WHERE id_cita = %s", id)

        #   I make the commit
        conexion_db.commit()

        #   I show the information messages
        print("Registro eliminado exitosamente en la tabla cita")
        print(cursorDeleteAngular.rowcount, "registro eliminado.")

        #   I close the cursor
        cursorDeleteAngular.close()
        
    except mysql.connector.Error as err:
        print("Error executing query")
        print(err)

    return jsonify('User deleted successfully!')

#   --- I DELETE HOUR FROM ANGULAR  ------------------------------------
@app.route('/deleteH/<id>',  methods=['delete'])
def DeleteFromHourAngular(id):

    try:
        #   I create the cursor
        cursorDeleteHourAngular = conexion_db.cursor()

        #   I execute the query
        cursorDeleteHourAngular.execute("DELETE FROM horario WHERE id_horario = %s", id)

        #   I make the commit
        conexion_db.commit()

        #   I show the information messages
        print("Registro eliminado exitosamente en la tabla horario")
        print(cursorDeleteHourAngular.rowcount, "registro eliminado.")

        #   I close the cursor
        cursorDeleteHourAngular.close()
        
    except mysql.connector.Error as err:
        print("Error executing query")
        print(err)

    return jsonify('User deleted successfully!')

#   --- I MAKE THE MAIN -------------------------------------------------------
if __name__ == '__main__':

    #   I start the APP
    app.run(debug = False, port = 5000)