#------------------------------------------------------------------------------
#               Created by: IMANOL VILLALBA
#               On: 06/05/2019
#------------------------------------------------------------------------------

#! / usr / bin / python3
# - * - codificación: utf-8 - * -

#   --- IMPORTS    ------------------------------------------------------------
import requests, os, pymysql, time
from flask import Flask, request, make_response, jsonify
from datetime import datetime

try:
    #   opens the database connection
    conexion_db = pymysql.connect("localhost", "admin", "123456", "barberia_bd")

except MySQL.Error as mysql_error:
    print ("Error connecting to database: %s" % (str(mysql_error)))

#   --- MAKE DE APP WITH FLASK  -----------------------------------------------
app = Flask(__name__)

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

    except MySQL.Error as mysql_error:
        print ("Error executing query: %s" % (str(mysql_error)))

#   --- MYSQL CONEXION  -------------------------------------------------------
def MySQL(fecha, hora, telefono):

    try:
          #   I create the cursor
        cursorMySQL = conexion_db.cursor()

        #   I execute the query
        query = "INSERT INTO `cita` (`fecha`,`hora`,`telefono`) VALUES (%s,%s,%s)"
        insert_tuple = (fecha, hora, telefono)
        result  = cursorMySQL.execute(query, insert_tuple)

        #   I save the data in the database
        conexion_db.commit()

        #   I show the information messages
        print("Registro insertado exitosamente en la tabla cita")
        print(cursorMySQL.rowcount, "registro insertado.")

        #   I close the cursor
        cursorMySQL.close()

    except MySQL.Error as mysql_error:
        print ("Error executing insert query: %s" % (str(mysql_error)))

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

    except MySQL.Error as mysql_error:
        print ("Error executing query: %s" % (str(mysql_error)))

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

#   --- I MAKE THE MAIN -------------------------------------------------------
if __name__ == '__main__':

    #   I start the APP
    app.run(debug = False, port = 5000)