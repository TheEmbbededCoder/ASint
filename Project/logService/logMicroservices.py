from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
from flask import send_file, send_from_directory, safe_join, abort
import requests
import json
import os
import glob, os



for file in glob.glob("*.log"):
	os.remove(file)

app = Flask(__name__)

def jprint(obj):
	# create a formatted string of the Python JSON object
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

@app.route('/add', methods=["POST"])
def add_log():
	message = {}
	if request.method == 'POST':
		if request.form.get('date') != "" and request.form.get('method') != "" and request.form.get('args') != "" and request.form.get('request') != "" and request.form.get('microservice') != "":
			try:
				data = {
					'date' : request.form['date'],
					'method' : request.form['method'],
					'args' : request.form['args'],
					'request' : request.form['request']
				}
				print("LOGGED")
				print(request.form['microservice'])
				# Write to file
				with open('log' + request.form['microservice'] + ".log", 'a') as file:
					file.write(json.dumps(data))
					file.write("\n")
					file.close()
				

				message = {
					'status_code': 200,
					'message'    : 'OK'
				}	
			except:
				message = {
					'status_code': 404,
					'message': 'Not able to log ' + request.form['microservice']
				}
	
	return jsonify(message)

@app.route('/log/<microservice>', methods=["GET"])
def get_log(microservice):
	message = {}
	try:
		print('log' + microservice + ".log")
		with open('log' + microservice + ".log", 'r') as log_file:
			log_data = log_file.readlines()
		
		log = {
			'microservice'   : microservice,
			'log'   : str(log_data)
		}
		message = {
			'status_code': 200,
			'message'    : 'OK',
			'log' : log
		}	
		print(message)	
	except:
		message = {
			'status_code': 404,
			'message': 'Unable to Read log for the ' + microservice,
			'log': None
		}
	return jsonify(message)


if __name__ == '__main__':
	app.run(debug=True, port=43000)
 