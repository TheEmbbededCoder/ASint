from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
from flask_caching import Cache
from flask_cors import CORS
import requests
import json

app_id = "1695915081465946" # copy value from the app registration
app_secret = "uKZBJ293qtOU6uQW7zPV0lrPQkgJ1kuY+56qKUtCavR/7KTTeuD8N+yeuNVy3+cT7qGhhDGRfH7Et5Ha067niQ=="
fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

users = {}
key = 0

admin_data = {
				'user' : "admin",
				'password' : "admin"
			}

microservices = {
	'canteen' : "http://127.0.0.1:42000/",
	'rooms' : "http://127.0.0.1:40000/",
	'secretariat' : "http://127.0.0.1:41000/"
}

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
CORS(app)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

def API_microServices(url, microS):
	try:
		resp = requests.get(url)
		if resp.status_code != 200:
			message = {
			'status_code': 404,
			'message': 'No resource found',
			str(microS): None
			}
		else:
			if(resp.json()[microS] != None):
				message = {
				'status_code': 200,
				'message': 'OK',
				str(microS): resp.json()[microS]
				}
			else:
				message = {
				'status_code': 200,
				'message': 'Resource not found at microservice',
				str(microS): None
				}
	except:
		message = {
			'status_code': 404,
			'message': 'Unable to perform API request to ' + str(microS) + ' microservice.',
			str(microS): None
		}
	return message


# ERROR resource not found page
@app.errorhandler(404)
def page_not_found(e):
	return render_template('serviceOfflineTemplate.html', type="found", services = microservices, login = user, key = key)


@app.route('/favicon.ico')
def favicon():
	return redirect(url_for('static', filename='favicon.ico'), code=302)

############ HTML #############
@app.route('/', methods=['GET'])
def homePage():
	if request.method == "GET":
		key = request.args.get("key")
		# User is login, perform actions accordingly to it
		if key in users:
			return render_template("index.html", services = microservices, login = users[key]['user'], key = key)
		else:
			return render_template("index.html", services = microservices, login = -1)
	return render_template("index.html", services = microservices, login = -1)

### Microservices

@app.route('/<path:subpath>')
#@cache.cached(timeout=50)
def html(subpath):
	if request.method == "GET":
		key = request.args.get("key")
		# User is login, perform actions accordingly to it
		if key in users:
			user = users[key]['user']
		else:
			user = -1
	microS = subpath.split('/')[0]
	template = microS + "Template.html"
	response = API(subpath)
	json = response[microS]
	if json == None:
		return render_template("serviceOfflineTemplate.html", service=microS, type="available", services = microservices, login = user, key = key)
	else:
		return render_template(template, microservice=microS, json=json, services = microservices, login = user, key = key)

### ADMIN
@app.route('/admin')
def admin():
	return render_template("adminTemplateLogin.html", services = microservices, error = False, login = -1)

@app.route('/adminLogin', methods=['POST'])
def adminLogin():
	if request.method == "POST":
		if "uname" in request.form and "psw" in request.form:
			admin_user = request.form["uname"]
			admin_pass = request.form["psw"]

			# User is authenticated
			if(admin_user == admin_data['user'] and admin_pass == admin_data['password']):
				if "name" in request.form:
					Name = request.form["name"]
					if int(request.form["delete"]) == 0:
						Location = request.form["location"]
						Description = request.form["description"]
						OpeningHours = request.form["hours"]
						data = {
								'name': Name, 
								'location': Location,
								'description': Description,
								'hours' : OpeningHours
								} 

					req = None
					try:
						if int(request.form["edit"]) == 0 and int(request.form["delete"]) == 0:
							# sending post request and saving response as response object 
							req = requests.post(url = microservices['secretariat'] + "secretariat/add/" + Name, data = data) 
						elif int(request.form["delete"]) == 1:
							data = {
								'name': Name, 
								'delete': 1
								} 
							# sending put request and saving response as response object 
							req = requests.put(url = microservices['secretariat'] + "secretariat/add/" + Name, data=data)
						else:
							data['delete'] = 0
							# sending put request and saving response as response object 
							req = requests.put(url = microservices['secretariat'] + "secretariat/add/" + Name, data=data)
						
						if req.status_code != 200:
							print(req.text)
							raise Exception('Recieved non 200 response while sending response to CFN.')
							return
					except requests.exceptions.RequestException as e:
						if req != None:
							print(req.text)
						print(e)
						raise 

				response = API("secretariat")
				secretariats = response["secretariat"]
				# Mostrar pagina de administração
				return render_template("adminTemplate.html", services = microservices, secretariats = secretariats, admin_user = admin_user, admin_pass = admin_pass, login = -1, admin = 1)
		
	return render_template("adminTemplateLogin.html", error = True)

@app.route('/EditSecretariat', methods=['POST'])
def EditSecretariat():
	if request.method == "POST":
		if "uname" in request.form and "psw" in request.form and "name" in request.form:
			admin_user = request.form["uname"]
			admin_pass = request.form["psw"]
			Name = request.form["name"]
			# User is authenticated
			if(admin_user == admin_data['user'] and admin_pass == admin_data['password']):
				response = API("secretariat/" + Name)
				secretariats = response["secretariat"]

				# Mostrar pagina de administração
				return render_template("adminEditTemplate.html", name=Name, services = microservices, secretariats = secretariats, admin_user = admin_user, admin_pass = admin_pass)
		
###########

### Login User

@app.route('/login', methods=['GET'])
def login():
	# Get the current global key
	login = False
	if request.method == "GET":
		try:
			key = int(request.args['key'])
			login = True
		except Exception as e:
			pass
	else:
		print("no get")

	if login == False:
		redPage = fenixLoginpage % (app_id, request.host_url + "userAuth")
		# the app redirecte the user to the FENIX login page
		return redirect(redPage)
	else:
		if str(key) in users:
			print("user authenticated")
			return redirect('/?key=' + str(key))
		else:
			return redirect('/login')

@app.route('/userAuth')
def userAuthenticated():
	# Get the current global key
	global key

	# Pede acesso ao fenix para o novo utilizador
	code = request.args['code']
	payload = {'client_id': app_id, 'client_secret': app_secret, 'redirect_uri' : request.host_url + "userAuth", 'code' : code, 'grant_type': 'authorization_code'}
	response = requests.post(fenixacesstokenpage, params = payload)

	if(response.status_code == 200):
		# get the user token
		r_token = response.json()['access_token']

		# Get FENIX user information
		params = {'access_token': r_token}
		resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
		if(resp.status_code == 200):
			r_info = resp.json()
			users[str(key)] = {
								'user' : r_info['username'],
								'token' : r_token
							 }
		else:
			# Not able to get user info
			users[str(key)] = {
								'token' : r_token
							 }

		# Increments the global key
		key = key + 1

		return redirect('/login?key=' + str(key - 1))
	else:
		print("Not able to authenticate")

	return redirect('/login')

#######

# ########## REST API ###########

@app.route('/API/<path:subpath>')
def API(subpath):
	microS = subpath.split('/')[0]
	url = microservices[microS] + subpath

	message = API_microServices(url, microS)
	return message

if __name__ == '__main__':
	app.run(debug=True, port=39000)
