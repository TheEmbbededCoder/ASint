from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import json
from flask_cors import CORS

import requests

app = Flask(__name__)
CORS(app)

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
		'microservice' : 'canteen',
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

@app.route('/canteen')
def API_showAll():
	try:
		# Show all canteens
		resp = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen')
		if resp.status_code != 200:
		    # This means something went wrong.
		    message = {
					'status_code': 404,
					'message': 'Canteen Fenix API is down',
					'canteen': None
				}
		else:
			canteen = resp.json()
			# Order the canteen menu by days
			ordered_canteen = sorted(canteen, key = lambda i: i['day']) 
			if canteen == None:
				message = {
						'status_code': 404,
						'message': 'No resource found',
						'canteen': None
					}
			else:
				message = {
						'status_code': 200,
						'message': 'Canteen in up',
						'canteen': ordered_canteen
					}
	except:
		message = {
			'status_code': 404,
			'message': 'Canteen Fenix API is down',
			'canteen': None
			}
	return jsonify(message)

@app.route('/canteen/<day>/<month>/<year>')
def API_showCanteen(day, month, year):
	date = day + '/' + month + '/' + year
	try:
		resp = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen')
		if resp.status_code != 200:
		    # This means something went wrong.
		    message = {
			'status_code': 404,
			'message': 'Canteen Fenix API is down',
			'canteen': None
			}
		else:
			canteen = resp.json()
			if canteen == None:
				message = {
				'status_code': 404,
				'message': 'No resource found',
				'canteen': None
				}
			else:
				output = []
				for d in canteen:
					if d['day'] == date:
						output.append(d)
				if output == None:
					message = {
					'status_code': 404,
					'message': 'No menu for the selected day found',
					'canteen': None
					}
				else:
					message = {
					'status_code': 200,
					'message': 'OK',
					'canteen': output
					}
	except:
		message = {
			'status_code': 404,
			'message': 'Canteen Fenix API is down',
			'canteen': None
			}
	return jsonify(message)
	


if __name__ == '__main__':
	app.run(debug=True, port=42000)
