from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import json

import requests

app = Flask(__name__)

########## REST API ###########

@app.route('/canteen')
def API_showAll():
	# Show all canteens
	resp = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen')
	canteen = resp.json()
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
		'canteen': canteen
		}
	return jsonify(message)

@app.route('/canteen/<day>/<month>/<year>')
def API_showCanteen(day, month, year):
	date = day + '/' + month + '/' + year
	print(date)
	resp = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen')
	if resp.status_code != 200:
	    # This means something went wrong.
	    pass
	else:
	    print(resp)
	
	canteen = resp.json()
	output = None
	for d in canteen:
		if d['day'] == date:
			output = d
	if output == None:
		message = {
		'status_code': 404,
		'message': 'No resource found',
		'canteen': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'canteen': output
		}
	return message
	


if __name__ == '__main__':
	app.run(debug=True, port=42000)
