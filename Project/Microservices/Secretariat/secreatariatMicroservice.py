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
		'secretariat': secr
		}
	return jsonify(message)

@app.route('/secretariat/<name>/description')
def API_getDescription(name):
	print("description")
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
			'secretariat': secr
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
		'secretariat': secr
		}
	return jsonify(message)

@app.route('/secretariat/add/<Location>/<Name>/<Description>/<OpeningHours>')
def API_add(Location, Name, Description, OpeningHours):
	print("Add")
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
		message = {
			'status_code': 200,
			'message': 'secretariat added',
			'secretariat': secretariat
			}
	return jsonify(message)

if __name__ == '__main__':
	app.run(debug=True, port=41000)
