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
	secr = db.listAllSecretariats()
	message = {}
	if secr == None:
		message = {
		'status_code': 404,
		'message': 'No resource found',
		'secretariats': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'secretariats': secr
		}
	return jsonify(message)

@app.route('/secretariat/<name>')
def API_show(name):
	secr = db.showSecretariat(name)
	message = {}
	if secr == None:
		message = {
		'status_code': 404,
		'message': 'No resource found',
		'secretariats': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'secretariats': secr
		}
	return jsonify(message)

@app.route('/secretariat/<name>/location')
def API_getLocation(name):
	secr = db.getLocation(name)
	message = {}
	if secr == None:
		message = {
		'status_code': 404,
		'message': 'No resource found',
		'secretariats': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'secretariats': secr
		}
	return jsonify(message)

@app.route('/secretariat/<name>/description')
def API_getDescription(name):
	secr = db.getDescription(name)
	message = {}
	if secr == None:
		message = {
		'status_code': 404,
		'message': 'No resource found',
		'secretariats': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'secretariats': secr
		}
	return jsonify(message)

@app.route('/secretariat/<name>/openhours')
def API_getOpenhours(name):
	secr = db.getOpenhours(name)
	message = {}
	if secr == None:
		message = {
		'status_code': 404,
		'message': 'No resource found',
		'secretariats': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'secretariats': secr
		}
	return jsonify(message)

if __name__ == '__main__':
	app.run(debug=True, port=41000)
