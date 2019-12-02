from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import requests
import json

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
			message = {
			'status_code': 200,
			'message': 'OK',
			str(microS): resp.json()[microS]
			}
	except:
		message = {
			'status_code': 404,
			'message': 'Unable to perform API request to ' + str(microS) + ' microservice.',
			str(microS): None
		}
	return message

app = Flask(__name__)

############ HTML #############

# SECRETARIAT
@app.route('/secretariat')
def secretariat_base():
	response = API_secretariat_base()
	secretariat = response['secretariats']
	if secretariat == None:
		return render_template("serviceOfflineTemplate.html", service="Secretariat", type="available")
	else:
		return render_template("secretariatListTemplate.html", sc=len(secretariat), secretariat=secretariat)

@app.route('/secretariat/<str>')
def secretariat(str):
	response = API_secretariat(str)
	secretariat = response['secretariats']
	if secretariat == None:
		return render_template("serviceOfflineTemplate.html", service="Secretariat", type="found")
	else:
		return render_template("secretariatTemplate.html", s=secretariat)

@app.route('/secretariat/<str>/<attr>')
def secretariat_attr(str, attr):
	url = str + '/' + attr
	response = API_secretariat(url)
	secretariat = response['secretariats']
	if secretariat == None:
		return render_template("serviceOfflineTemplate.html", service="Secretariat", type="found")
	else:
		return render_template("secretariatAttrTemplate.html", attr=attr, value=secretariat)

# ROOMS
@app.route('/rooms')
def rooms_base():
	response = API_rooms_base()
	if response['message'] == 'OK':
		return render_template("roomsListTemplate.html")
	else:
		return render_template("roomsOfflineTemplate.html", service="Room", type="available")


@app.route('/rooms/<str>')
def rooms(str):
	response = API_rooms(str)
	campi=response['rooms']['campi']
	building=response['rooms']['building']
	
	if response['message'] == 'OK':
		return render_template("roomsInformation.html", campi=campi, building=building, id=str)
	else:
		return render_template("roomsOfflineTemplate.html", service="Room", type="available")

#CANTEEN

@app.route('/canteen')
def canteen_base():
	response = API_canteen_base()
	if response["canteen"] == None:
		return render_template("serviceOfflineTemplate.html", service="Canteen", type="found")
	else:
		return render_template("canteenListTemplate.html", canteen = response["canteen"])

@app.route('/canteen/<day>/<month>/<year>')
def canteen(day, month, year):
	response = API_canteen(day, month, year)
	if response["canteen"] == None:
		return render_template("serviceOfflineTemplate.html", service="Canteen", type="found")
	else:
		return render_template("canteenDayTemplate.html", canteen = response["canteen"])

# ERROR resource not found page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('serviceOfflineTemplate.html', type="found")

########## REST API ###########
# ------------------------------#
@app.route('/API/secretariat')
def API_secretariat_base():
	message = {}
	url = "http://127.0.0.1:41000/secretariat"

	message = API_microServices(url, "secretariats")

	return message

@app.route('/API/secretariat/<str>')
def API_secretariat(str):
	message = {}
	url = "http://127.0.0.1:41000/secretariat/" + str
	
	message = API_microServices(url, "secretariats")
	return message

# ------------------------------#
@app.route('/API/rooms')
def API_rooms_base():
	message = {}
	url = "http://127.0.0.1:40000/rooms"

	message = API_microServices(url, "rooms")
	return message

@app.route('/API/rooms/<str>')
def API_rooms(str):
	message = {}
	url = "http://127.0.0.1:40000/rooms/" + str
	
	message = API_microServices(url, "rooms")
	return message
	
# ------------------------------#
@app.route('/API/canteen')
def API_canteen_base():
	message = {}
	url = "http://127.0.0.1:42000/canteen"

	message = API_microServices(url, "canteen")
	return message

@app.route('/API/canteen/<day>/<month>/<year>')
def API_canteen(day, month, year):
	message = {}
	url = "http://127.0.0.1:42000/canteen/" + day + "/" + month + "/" + year
	print(url)
	message = API_microServices(url, "canteen")
	return message

if __name__ == '__main__':
	app.run(debug=True, port=39000)
