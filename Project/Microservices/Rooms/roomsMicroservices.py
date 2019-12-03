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
	message = {
			'status_code': 200,
			'message': 'OK',
			'rooms': "Rooms is up"
			}
	return jsonify(message)

@app.route('/rooms/<id>')
def room_location(id):
	message = {}
	try:
		resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(id))

		if resp.status_code != 200:
			#This means something went wrong.
			message = {
				'status_code': 404,
				'message': 'Resource not found',
				'rooms': None
			}
		else:
			pass_times = resp.json()
			jprint(pass_times['name'])
			jprint(pass_times['topLevelSpace']['name'])
			
			room_local = {
				'campi'      : pass_times['topLevelSpace']['name'],
				'building'   : pass_times['name']
			}
			message = {
				'status_code': 200,
				'message'    : 'OK',
				'rooms' : room_local
			}		
	except:
		message = {
			'status_code': 404,
			'message': 'Unable to perform API resquest to Fenix',
			'rooms': None
		}


	return jsonify(message)


@app.route('/rooms/<id>/<day>/<mouth>/<year>')
def rooms_timetable(id, day, mouth, year):
	message = {}
	try:
		resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(id)+"?day="+str(day)+"/"+str(mouth)+"/"+str(year))

		if resp.status_code != 200:
			#This means something went wrong.
			message = {
				'status_code': 404,
				'message': 'Resource not found',
				'rooms': None
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
				'rooms': room_timetable
			}
	except :
		message = {
			'status_code': 404,
			'message': 'Unable to perform API resquest to Fenix',
			'rooms': None
		}
	
	return jsonify(message)

if __name__ == '__main__':
	app.run(debug=True, port=40000)
 