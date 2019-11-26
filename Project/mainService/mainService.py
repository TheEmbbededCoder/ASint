from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import requests
import json

app = Flask(__name__)

############ HTML #############
@app.route('/secretariat')
def secretariat_base():
	response = API_secretariat_base()
	print(response)
	#secretariat = response.status_code
	#print(secretariat)
	return render_template("secretariatTemplate.html")

########## REST API ###########

@app.route('/API/secretariat')
def API_secretariat_base():
	print("secretariat base")
	message = {}
	try:
		url = "http://127.0.0.1:41000/secretariat"
		print(url)
		resp = requests.get(url)
		if resp.status_code != 200:
			message = {
			'status_code': 404,
			'message': 'No resource found',
			'secretariats': None
			}
		else:
			message = {
			'status_code': 200,
			'message': 'OK',
			'secretariats': resp.json()['secretariats']
			}
	except:
		message = {
		'status_code': 404,
		'message': 'Unable to perform API request to secretariats microservice',
		'secretariats': None
		}
	return jsonify(message)

@app.route('/API/secretariat/<str>')
def API_secretariat(str):
	print("secretariat")
	message = {}
	try:
		url = "http://127.0.0.1:41000/secretariat" + str
		print(url)
		resp = requests.get(url)
		if resp.status_code!= 200:
			message = {
			'status': 404,
			'message': 'No resource found',
			'secretariats': None
			}
		else:
			message = {
			'status': 200,
			'message': 'OK',
			'secretariats': resp.json()['secretariats']
			}
	except:
		message = {
		'status': 404,
		'message': 'Unable to perform API request to secretariats microservice',
		'secretariats': None
		}
	return jsonify(message)

@app.route('/API/rooms')
def API_rooms_base():
	print("rooms base")
	message = {}
	try:
		url = "http://127.0.0.1:40000/rooms"
		print(url)
		resp = requests.get(url)
		if resp.status_code != 200:
			message = {
			'status': 404,
			'message': 'No resource found',
			'rooms': None
			}
		else:
			message = {
			'status': 200,
			'message': 'OK',
			'rooms': resp.json()['room']
			}
	except:
		message = {
		'status': 404,
		'message': 'Unable to perform API request to rooms microservice',
		'rooms': None
		}
	return jsonify(message)


@app.route('/API/rooms/<str>')
def API_rooms(str):
	print("rooms")
	message = {}
	try:
		url = "http://127.0.0.1:40000/rooms/" + str
		print(url)
		resp = requests.get(url)
		if resp.status_code!= 200:
			message = {
			'status': 404,
			'message': 'No resource found',
			'room': None
			}
		else:
			message = {
			'status': 200,
			'message': 'OK',
			'room': resp.json()['room']
			}
	except:
		message = {
		'status': 404,
		'message': 'Unable to perform API request to rooms microservice',
		'room': None
		}
	return jsonify(message)

@app.route('/API/canteen')
def API_canteen_base():
	print("canteen base")
	message = {}
	try:
		url = "http://127.0.0.1:42000/canteen"
		print(url)
		resp = requests.get(url)
		if resp.status_code!= 200:
			message = {
			'status': 404,
			'message': 'No resource found',
			'canteen': None
			}
		else:
			message = {
			'status': 200,
			'message': 'OK',
			'canteen': resp.json()['canteen']
			}
	except:
		message = {
		'status': 404,
		'message': 'Unable to perform API request to canteen microservice',
		'canteen': None
		}
	return jsonify(message)

@app.route('/API/canteen/<str>')
def API_canteen(str):
	print("canteen")
	message = {}
	try:
		url = "http://127.0.0.1:42000/canteen/" + str
		print(url)
		resp = requests.get(url)
		if resp.status_code!= 200:
			message = {
			'status': 404,
			'message': 'No resource found',
			'canteen': None
			}
		else:
			message = {
			'status': 200,
			'message': 'OK',
			'canteen': resp.json()['canteen']
			}
	except:
		message = {
		'status': 404,
		'message': 'Unable to perform API request to canteen microservice',
		'canteen': None
		}
	return jsonify(message)

if __name__ == '__main__':
	app.run(debug=True, port=39000)
