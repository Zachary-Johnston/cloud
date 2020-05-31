from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response

import mysql.connector as mysql
import requests
import json
import os
import time
import paho.mqtt.client as mqtt


db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

# Show all the users in the database
def show_users(req):
  # "/users" comes from the route defined in rest_server.py
  #Users = requests.get(REST_SERVER + "/users").json()
  Users = requests.get('https://64.225.127.211:6001/users').json()
  # The word "users" is a variable that is used in the show_users.html
  return render_to_response('templates/show_users.html', {'users': Users}, request=req)












def setcoffeex(req):
  print("BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
  temperature=req.params["temperature"]
  print(temperature)
  date=req.params["date"]
  print(date)
  time=req.params["time"]
  print(time)
  recur=req.params["recur"]
  print(recur)

 
  data = {"temperature": temperature, "date": date, "time": time, "recur": recur}
  print("rannnnn2")
  print(data)

  coffeetemp = requests.post(REST_SERVER + '/coffeeset', data=data).json()
  print("whatalifemann")
  return render_to_response('templates/timer.html', {}, request=req)









#def coffeeset(req):
 # View the Dictionary that was Posted
 # Get the fname
 #print("bbbeeeeeppppp")
 #temp = str(req.params.getall("temperature"))
 # Get rid of the [] that comes from req
 #print(temp)
 #start = time.time()
 #print(start)
 #temp = temp[2:len(temp)-2]
 #print(temp)
 #db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
 #cursor = db.cursor()
 # Insert Records
 #query = "insert into cofset (coffeeid, temperature, time) values (%s, %s, %s)"
 #values = [
 #("testid", temp, start),
 #]
 #print("GOT THIS FAR1")
 #cursor.executemany(query, values)
 #db.commit()
 #print("GOT THIS FAR2")
 #cursor.execute("SELECT coffeeid, temperature, time from cofset;")
 #records = cursor.fetchall()
 #print(records)
 #return timer(req)
  
  
def coffeeset(req):
  # View the Dictionary that was Posted
  # Get the fname
  print("bbbeeeeeppppp")
  temp = str(req.params.getall("temperature"))
  date = str(req.params.getall("date"))
  time = str(req.params.getall("time"))
  recur = str(req.params.getall("recur"))
  # Get rid of the [] that comes from req
  temp = temp[2:len(temp)-2]
  date = date[2:len(date)-2]
  time = time[2:len(time)-2]
  recur = recur[2:len(recur)-2]
  msg ='{"temperature": "'+temp+'", "date": "' +date+ '", "time": "'+time+'", "recur": "'+recur+'"}'
  print(msg)
  # SEND TO RASPBERRY PI WITH MQTT
  client = mqtt.Client("JJJ")
  client.connect("polarcoffee.org", port=1883, keepalive=60, bind_address="")
  client.publish("test", msg)
  return render_to_response('templates/timer.html', {}, request=req)
  #SEND TO DATABASE
  #db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  #cursor = db.cursor()
  # Insert Records
  #query = "insert into cofset (coffeeid, temperature, time) values (%s, %s, %s)"
  #values = [
  #("testid", temp, time),
  #]
  #print("GOT THIS FAR1")
  #cursor.executemany(query, values)
 # db.commit()
 # print("GOT THIS FAR2")
  #cursor.execute("SELECT coffeeid, temperature, time from cofset;")
  #records = cursor.fetchall()
  #print(records)


def setcoffee(req):
  return render_to_response('templates/setter.html', {'username': req.params['username']}, request =req)




############################################

def get_members(req):
  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select count(id) from Users;")
  records = cursor.fetchall()
  db.close()
  value_to_return = {}
  value_to_return['records'] = records[0]
  value_to_return = Response(body=json.dumps(value_to_return))
  #records = records[1:len(records)-1]
  print(records)
  return value_to_return

############################################

############################################

def get_news(req):
  # Connect to the database and retrieve the news
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from newsupdates;")
  record = cursor.fetchall()
  db.close()
  value_to_return = {}
  value_to_return['record'] = record
  value_to_return = Response(body=json.dumps(value_to_return))
  #record = record[1:len(record)-1]
  print(record)
  return value_to_return

############################################

def portal(req):
  return render_to_response('templates/portal.html', {}, request =req)

############################################


def get_ready(req):
  # Connect to the database and retrieve the news
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select days from ready where id=1;")
  recorded = cursor.fetchall()
  db.close()
  value_to_return = {}
  value_to_return['recorded'] = recorded
  value_to_return = Response(body=json.dumps(value_to_return))
  #record = record[1:len(record)-1]
  print(recorded)
  return value_to_return







def add_new_user(req):
  # Get all the data that is going to be sent (needs to be a dict like "data")
  # print(req.params) #debugging
  data = {"Username": req.params['Username'], "Password":  req.params['Password']}
  #New_user = requests.post(REST_SERVER + '/new_users', data=data).json()
  New_user = requests.post('https://64.225.127.211:6001/new_users', data=data).json()
  return render_to_response('templates/portal.html', {}, request=req)

def add_users_db(req):
  # View the Dictionary that was Posted
  # Get the Password
  newPsw = str(req.params.getall("Password"))
  # Get rid of the [] that comes from req
  newPsw = newPsw[2:len(newPsw)-2]
  # Get the name the user entered
  newName = str(req.params.getall("Username"))
  # Get rid of the [] that comes from req
  newName = newName[2:len(newName)-2]
  # Connect to the database
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  # Insert Records
  query = "insert into Users (Username, Password, Status) values (%s, %s, %s)"
  values = [
  (newName,newPsw,'Pending'),
  ]
  cursor.executemany(query, values)
  db.commit()
  cursor.execute("SELECT Username, Password, Status from Users;")
  records = cursor.fetchall()
  json.dumps(records) #take this out?
  return render_to_response('templates/portal.html', {}, request =req)

# This function will become useless
def changestatus(req):
  # Get all the data that is going to be sent (needs to be a dict like "data")
  # current does not run since all info is being sent to the Rest server
  print("1 *****************************************************")
  print(req.json_body)
  info_to_send = req.json_body
  print("2 *****************************************************")
  print(info_to_send)

 # data = {"Username": info_to_send['Username'],
  #        "Status": info_to_send['Status']}
  #newstatus = requests.post(REST_SERVER + '/change_status', data = data).json()
  return render_to_response('templates/did_log_in.html', {}, request =req)
  #return True



# Compare credentials from request (from user) to json
def correct_password(req):
  data = {"Username": req.params['Username'], "Password":  req.params['Password']}
  #validity = requests.post(REST_SERVER + '/check_password', data = data).json()
  validity = requests.post('https://64.225.127.211:6001/check_password', data = data).json()
  return validity

def valid_user(req):
  try:
    data = {"Username": req.params['Username']}
  except:
    data = req
  #validity = requests.post(REST_SERVER + '/check_validity', data = data).json()
  validity = requests.post('https://64.225.127.211:6001/check_validity', data = data).json()
  return validity

# Route to validate login credentials...
def post_login(req):
  if valid_user(req) and correct_password(req):
    return menuportal(req)#controller(req)#
  else:
    return render_to_response('templates/did_log_in.html', {'tag': 'Incorrect Password'}, request = req)

# These currently just render the html files 
def sign_up(req):
  return render_to_response('templates/sign_up.html', {}, request =req)

def about(req):
  return render_to_response('templates/about.html', {}, request =req)

def pricing(req):
  return render_to_response('templates/pricing.html', {}, request =req)

def features(req):
  return render_to_response('templates/features.html', {}, request =req)
 
def login(req):
  return render_to_response('templates/did_log_in.html', {}, request =req)

def metrics(req):
  return render_to_response('templates/metrics.html', {}, request =req)









def setter(req):
  return render_to_response('templates/setter.html', {}, request =req)

def timer(req):
  return render_to_response('templates/timer.html', {}, request =req)








def admin(req):
  #Users = requests.get(REST_SERVER + "/users").json()
  Users = requests.get("https://64.225.127.211:6001/users").json()
  return render_to_response('templates/adminportal.html',{'users': Users}, request =req)

def tracker(req):
  #moves = requests.get(REST_SERVER + "/requested_moves").json()
  moves = requests.get("https://64.225.127.211:6001/requested_moves").json()
  return render_to_response('templates/tracker.html', {'Username': req.params['Username'], 'moves': moves}, request =req)
 
def controller(req):
  return render_to_response('templates/controller.html', {'Username': req.params['Username']}, request =req)

def menuportal(req):
  return render_to_response('templates/menuportal.html', {'Username': req.params['Username']}, request =req)

def post_menu(req):
  data = {"nextLocation":  req.params['input'], "Username": req.params['Username']}
  if valid_user(data):
    if data['nextLocation'] == 'Tracker':
      return tracker(req)
    if data['nextLocation'] == 'Controller':
      return controller(req)
    if data['nextLocation'] == 'admin':
      return admin(req)
    if data['nextLocation'] == 'about':
      return about(req)

  return render_to_response('templates/did_log_in.html', {}, request =req)

''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('v2', '/')
  # Loading stuff from the server
  config.add_view(portal, route_name='v2') #change to controller

  config.add_route('show_users', '/show_users')
  config.add_view(show_users, route_name='show_users')  

  config.add_route('changestatus', '/change_status')
  #config.add_view(changestatus, route_name='changestatus')
  config.add_view(changestatus, route_name='changestatus', request_method = "POST")

  config.add_route('new_user', '/new_user')
  #For view users(quick debugging)
  #config.add_view(show_users, route_name='new_user')
  # What send info over to the Rest Server
  config.add_view(add_new_user, route_name='new_user', request_method = "POST")

  config.add_route('sign_up', '/sign_up')
  config.add_view(sign_up, route_name='sign_up')
  
   ##########ADDED
  config.add_route('add_new_user', '/new_users')
  config.add_view(add_users_db, route_name='add_new_user', renderer='json')
  

  config.add_route('login', '/login')
  config.add_view(login, route_name='login')
 
  config.add_route('post_login', '/post_login')
  config.add_view(post_login, route_name='post_login', request_method = "POST")
  
  config.add_route('tracker', '/tracker') # Added route for tracker 
  config.add_view(tracker, route_name='tracker')
  
  config.add_route('menuportal', '/menuportal') # Added route for menuportal
  config.add_view(menuportal, route_name='menuportal')

  config.add_route('about', '/about') # Added route for about
  config.add_view(about, route_name='about')
  
  config.add_route('features', '/features') # Added route for features
  config.add_view(features, route_name='features')
  
  config.add_route('pricing', '/pricing') # Added route for pricing
  config.add_view(pricing, route_name='pricing')

  config.add_route('post_menu', '/post_menu')
  config.add_view(post_menu, route_name='post_menu', request_method = "POST")
  
  config.add_route('metrics', '/metrics') # Added route for metrics rendering
  config.add_view(metrics, route_name='metrics')
  
  
  
  
  
  
  config.add_route('setter', '/setter') # Added route for setter
  config.add_view(setter, route_name='setter')
  
  config.add_route('timer', '/timer') # Added route for timer
  config.add_view(timer, route_name='timer')
  
  config.add_route('coffeeset', '/coffeeset') # Added route for timer
  config.add_view(coffeeset, route_name='coffeeset')
  
  config.add_route('setcoffeex', '/setcoffeex') # Added route for timer
  config.add_view(setcoffeex, route_name='setcoffeex')
  
  
  
  
  ##################################
  
  config.add_route('get_members', '/get_members')
  config.add_view(get_members, route_name='get_members', renderer='json')
  
  ##################################
  
  ##################################
  
  config.add_route('get_news', '/get_news')
  config.add_view(get_news, route_name='get_news', renderer='json')
  
  ##################################
  
  ##################################
  
  config.add_route('get_ready', '/get_ready')
  config.add_view(get_ready, route_name='get_ready', renderer='json')
  
  ##################################



  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
