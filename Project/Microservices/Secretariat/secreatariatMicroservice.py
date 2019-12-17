from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import secretariatsDB
import secretariats


app = Flask(__name__)
db = secretariatsDB.secretariatsDB("secretariats")
for secretariat in db.listAllSecretariats():
	print(secretariat)



############ LOG #############
import datetime 
import requests
log_microservice = "http://127.0.0.1:43000/"
@app.before_request
def before_request_func():
	args = request.args.get("key")
	if args == None:
		args = "Undefined User"
	if args == "":
		args = "Undefined User"
	
	data = {
		'date' : str(datetime.datetime.now()),
		'method' : request.method,
		'microservice' : 'secretariat',
		'args' : args,
		'request' : str(request)
	}
	try:
		req = requests.post(url = log_microservice + "add", data = data) 
		if req.status_code != 200:
			print("Log service not available")
	except Exception as e:
		print("ERROR - Logging"+str(e))

########## REST API ###########

@app.route('/secretariat')
def API_showAll():
	message = {}
	secretariats = db.listAllSecretariats()
	if secretariats == None:
		message = {
		'status_code': 404,
		'message': 'No secretariat found',
		'secretariat': None
		}
	else:
		secr_list = []
		for secr in secretariats:
			secretariat = {
				'Name' : secr.Name,
				'Location' : secr.Location,
				'Description' : secr.Description,
				'OpeningHours' : secr.OpeningHours
			}
			secr_list.append(secretariat)

		message = {
			'status_code': 200,
			'message': 'Secretariat is up',
			'secretariat': secr_list
			}
	return jsonify(message)

@app.route('/secretariat/<name>')
def API_show(name):
	secr = db.showSecretariat(name)
	if secr == None:
		message = {
			'status_code': 404,
			'message': 'No secretariat found',
			'secretariat': None
			}
	else:
		secretariat = {
			'Name' : secr.Name,
			'Location' : secr.Location,
			'Description' : secr.Description,
			'OpeningHours' : secr.OpeningHours
		}
		message = {
			'status_code': 200,
			'message': 'OK',
			'secretariat': secretariat
			}
	return jsonify(message)

@app.route('/secretariat/<name>/location')
def API_getLocation(name):
	secr = db.getLocation(name)
	message = {}
	if secr == None:
		message = {
		'status_code': 404,
		'message': 'No secretariat found',
		'secretariat': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'secretariat': {'location' : secr}
		}
	return jsonify(message)

@app.route('/secretariat/<name>/description')
def API_getDescription(name):
	secr = db.getDescription(name)
	print(secr)
	message = {}
	if secr == None:
		message = {
			'status_code': 404,
			'message': 'No secretariat found',
			'secretariat': None
			}
	else:
		message = {
			'status_code': 200,
			'message': 'OK',
			'secretariat': {'description' : secr}
			}
	return jsonify(message)

@app.route('/secretariat/<name>/openhours')
def API_getOpenhours(name):
	secr = db.getOpenhours(name)
	message = {}
	if secr == None:
		message = {
		'status_code': 404,
		'message': 'No secretariat found',
		'secretariat': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'secretariat': {'openhours' : secr}
		}
	return jsonify(message)

@app.route('/secretariat/add/<name>', methods=['POST', 'PUT'])
def API_add(name):
	if request.method == "POST":
		Name = request.form["name"]
		Location = request.form["location"]
		Description = request.form["description"]
		OpeningHours = request.form["hours"]

	elif request.method == "PUT":
		if db.showSecretariat(name) != None:
			if int(request.values['delete']) == 0:
				Name = name
				Location = request.get_json()["location"]
				Description = request.get_json()["description"]
				OpeningHours = request.get_json()["hours"]
			else:
				db.delSecretariat(name)
				message = {
						'status_code': 200,
						'message': 'secretariat deleted',
						'secretariat': None
					}
				return jsonify(message)
		else:
			message = {
						'status_code': 404,
						'message': 'No secretariat found',
						'secretariat': None
					}
			return jsonify(message)
		
	db.addSecretariat(Location, Name, Description, OpeningHours)
	secr = db.showSecretariat(Name)
	if secr == None:
		message = {
			'status_code': 404,
			'message': 'No secretariat added',
			'secretariat': None
			}
	else:
		secretariat = {
			'Name' : secr.Name,
			'Location' : secr.Location,
			'Description' : secr.Description,
			'OpeningHours' : secr.OpeningHours
		}
		if request.method == "POST":
			message = {
				'status_code': 200,
				'message': 'secretariat added',
				'secretariat': secretariat
				}
		elif request.method == "PUT":
			message = {
				'status_code': 200,
				'message': 'secretariat eddited',
				'secretariat': secretariat
				}

	return jsonify(message)


if __name__ == '__main__':
	app.run(debug=True, port=41000)
