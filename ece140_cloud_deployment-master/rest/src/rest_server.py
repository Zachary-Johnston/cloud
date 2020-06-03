from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import render_to_response

import json
import mysql.connector as mysql
import os
import requests
import time
import paho.mqtt.client as mqtt


                ##############################################################################
                #                 Including completed code from assignment API
                ##############################################################################
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']







def check_password_db(req):
  newPsw = str(req.params.getall("Password"))
  newPsw = newPsw[2:len(newPsw)-2]
  newName = str(req.params.getall("Username"))
  newName = newName[2:len(newName)-2]
  # Connect to the database
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  cursor.execute("SELECT Username from Users WHERE Username='%s';" % newName)
  userResult = cursor.fetchall()
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  cursor.execute("SELECT Password from Users WHERE Password='%s';" % newPsw)
  passwordResult = cursor.fetchall()
  passwordResult = str(passwordResult)
  passwordResult = passwordResult[3:len(newPsw)+3]
  userResult = str(userResult)
  userResult = userResult[3:len(newName)+3]
  print(userResult)
  if newName == userResult:
    if passwordResult == newPsw:
     return True
  return False


def validity_db(req):
  newName = str(req.params.getall("Username"))
  newName = newName[2:len(newName)-2]
  # Connect to the database
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  cursor.execute("SELECT Status from Users WHERE Username='%s';" % newName)
  validityResult = cursor.fetchall()
  validityResult = str(validityResult)
  validityResult = validityResult[3:8]
  print(validityResult)
  print(str(validityResult) == "Valid")
  if str(validityResult) == "Valid":
    return True
  return False







def coffeeset(req):
  # View the Dictionary that was Posted
  # Get the fname
  print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
  info = req.json_body
  print(info)

  msg = json.dumps(info)
  print(msg)
  # SEND TO RASPBERRY PI WITH MQTT
  client = mqtt.Client("JJJ")
  client.connect("polarcoffee.org", port=1883, keepalive=60, bind_address="")
  client.publish("test", msg)
  
  records = {}
  records['success'] = True
  records = Response(body=json.dumps(records))
  records.headers.update({'Access-Control-Allow-Origin': '*',})

  return records

if __name__ == '__main__':
  config = Configurator()

  config.add_route('coffeeset', '/coffeeset') # Added route for timer
  config.add_view(coffeeset, route_name='coffeeset')
  
  config.add_route('check_validity', '/check_password')
  config.add_view(check_password_db, route_name='check_validity', renderer='json')
  
  config.add_route('validity', '/check_validity')
  config.add_view(validity_db, route_name='validity', renderer='json')

              ##############################################################################
              #                        Adding Routes to Database                           #
              ##############################################################################



              ##############################################################################
              #                        --END OF CODE ---                                   #
              ##############################################################################
  

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
