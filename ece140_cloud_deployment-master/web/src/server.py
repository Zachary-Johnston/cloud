from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

import mysql.connector as mysql
import os

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

# Show all the users in the database
def show_users(req):
  # "/users" comes from the route defined in rest_server.py
  Users = requests.get(REST_SERVER + "/users").json()
  # The word "users" is a variable that is used in the show_users.html
  return render_to_response('templates/show_users.html', {'users': Users}, request=req)


def add_new_user(req):
  # Get all the data that is going to be sent (needs to be a dict like "data")
  # print(req.params) #debugging


  data = {"Username": req.params['Username'], "Password":  req.params['Password']}
  New_user = requests.post(REST_SERVER + '/new_users', data=data).json()
  return render_to_response('templates/portal.html', {}, request=req)

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
  validity = requests.post(REST_SERVER + '/check_password', data = data).json()
  return validity

def valid_user(req):
  try:
    data = {"Username": req.params['Username']}
  except:
    data = req
  validity = requests.post(REST_SERVER + '/check_validity', data = data).json()
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

def portal(req):
  return render_to_response('templates/portal.html', {}, request =req)
 
def login(req):
  return render_to_response('templates/did_log_in.html', {}, request =req)

def admin(req):
  Users = requests.get(REST_SERVER + "/users").json()
  return render_to_response('templates/adminportal.html',{'users': Users}, request =req)

def tracker(req):
  moves = requests.get(REST_SERVER + "/requested_moves").json()
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

  config.add_route('post_menu', '/post_menu')
  config.add_view(post_menu, route_name='post_menu', request_method = "POST")



  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()