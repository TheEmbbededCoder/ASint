from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify

import requests

app = Flask(__name__)

########## REST API ###########

@app.route('/cateen')
def API_showAll():
	# Show all canteens
	canteen = None
	if canteen == None:
		message = {
		'status_code': 404,
		'message': 'No resource found',
		'canteen': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'canteen': canteen
		}
	return jsonify(message)

@app.route('/cateen/<location>')
def API_showCateen(location):
	print('API_showCateen ' + str(location))
	resp = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/' + str(location) + '/canteen')
	if resp.status_code != 200:
	    # This means something went wrong.
	    pass
	else:
	    print(resp)
	canteen = None
	if canteen == None:
		message = {
		'status_code': 404,
		'message': 'No resource found',
		'canteen': None
		}
	else:
		message = {
		'status_code': 200,
		'message': 'OK',
		'canteen': canteen
		}
	return jsonify(message)
	
@app.route('/cateen/<location>/<day>/<mounth>/<year>')
def API_showMeal(location, day, mounth, year):
	# Show all canteens
	canteen = None
	if canteen == None:
		message = {
		'status': 404,
		'message': 'No resource found',
		'canteen': None
		}
	else:
		message = {
		'status': 200,
		'message': 'OK',
		'canteen': canteen
		}
	return jsonify(message)

if __name__ == '__main__':
	app.run()
