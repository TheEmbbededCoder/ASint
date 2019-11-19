from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify

app = Flask(__name__)

@app.route('/rooms')
def rooms():
	# SHOW ALL ROOMS EX
	return jsonify(result)

@app.route('/rooms/<id>')
def rooms_id(id):
	room = {
		'id' : id,
	}
	message = {
        'status': 200,
        'message': 'OK',
        'room': room
    }
	result = '/rooms' + str(id)
	return jsonify(message)


@app.route('/rooms/<id>/timetable/<day>/<mouth>/<year>')
def rooms_timetable(id, day, mouth, year):
	room_timetable = {
		'id'   : id,
		'day'  : day, 
		'mouth': mouth,
		'year' : year
	}
	message = {
        'status': 200,
        'message': 'OK',
        'room': room_timetable
    }
	
	return jsonify(message)

if __name__ == '__main__':
	app.run()
 