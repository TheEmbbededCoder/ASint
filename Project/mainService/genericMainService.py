from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
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

app = Flask(__name__)

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
	return render_template('serviceOfflineTemplate.html', type="found")


@app.route('/favicon.ico')
def favicon():
	return redirect(url_for('static', filename='favicon.ico'), code=302)

############ HTML #############
@app.route('/')
def homePage():
	return render_template("mainPage.html", services = microservices)

### ADMIN
@app.route('/admin')
def admin():
	return render_template("adminTemplateLogin.html", error = False)

@app.route('/adminLogin', methods=['POST'])
def adminLogin():
	if request.method == "POST":
		admin_user = request.form["uname"]
		admin_pass = request.form["psw"]

		# User is authenticated
		if(admin_user == admin_data['user'] and admin_pass == admin_data['password']):
			# Mostrar pagina de administração
			return render_template("adminTemplate.html")
		

	return render_template("adminTemplateLogin.html", error = True)

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
			return redirect('/?key=' + key)
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

### Microservices

@app.route('/<path:subpath>')
def html(subpath):
	microS = subpath.split('/')[0]
	template = microS + "Template.html"
	response = API(subpath)
	json = response[microS]
	if json == None:
		return render_template("serviceOfflineTemplate.html", service="Secretariat", type="found")
	else:
		return render_template(template, microservice=microS, json=json)

# ########## REST API ###########

@app.route('/API/<path:subpath>')
def API(subpath):
	microS = subpath.split('/')[0]
	url = microservices[microS] + subpath

	message = API_microServices(url, microS)
	return message

if __name__ == '__main__':
	app.run(debug=True, port=39000)
