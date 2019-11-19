from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import requests
import json

app = Flask(__name__)

def jprint(obj):
	# create a formatted string of the Python JSON object
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

@app.route('/rooms')
def rooms():
	# SHOW ALL ROOMS EX
	return jsonify(result)

@app.route('/rooms/<classroom>')
def room_location(classroom):
	message = {}
	try:
		resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/"+str(classroom)+"/spaces")

		if resp.status_code != 200:
			#This means something went wrong.
			message = {
				'status_code': 404,
				'message': 'Resource not found',
				'room': None
			}
		else:
			pass_times = resp.json()
			#jprint(resp.json())

			campi = []
			building = []
			for d in pass_times:
				campi.append(d['id'])
				building.append(d['name'])

			print(campi)
			print(building)

			room_local = {
				'campi'      : campi,
				'building'   : building
			}
			message = {
				'status_code': 200,
				'message'    : 'OK',
				'room_local' : room_local
			}		
	except:
		message = {
			'status_code': 404,
			'message': 'Unable to perform API resquest to Fenix',
			'room': None
		}


	return jsonify(message)


@app.route('/rooms/<classroom>/<id>/<day>/<mouth>/<year>')
def rooms_timetable(classroom, id, day, mouth, year):
	message = {}
	try:
		resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/"+str(classroom)+"/spaces/"+str(id)+"?day="+str(day)+"/"+str(mouth)+"/"+str(year))

		if resp.status_code != 200:
			#This means something went wrong.
			message = {
				'status_code': 404,
				'message': 'Resource not found',
				'room': None
			}
		else:
			# All events of that week
			pass_times = resp.json()['events']

			# Filtering by day required
			schedule = []
			for d in pass_times:
				if d['day'] == str(day)+"/"+str(mouth)+"/"+str(year):
					schedule.append(d['period'])

			room_timetable = {
				'id'      : id,
				'type'    : resp.json()['type'],
				'mouth'   : str(mouth),
				'year'    : str(year),
				'schedule': schedule
			}

			message = {
				'status_code': 200,
				'message': 'OK',
				'room': room_timetable
			}
	except :
		message = {
			'status_code': 404,
			'message': 'Unable to perform API resquest to Fenix',
			'room': None
		}
	
	return jsonify(message)

if __name__ == '__main__':
	app.run()
 