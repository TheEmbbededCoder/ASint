from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import requests
import json

microservices = {
	'canteen' : "http://127.0.0.1:42000/",
	'rooms' : "http://127.0.0.1:40000/",
	'secretariat' : "http://127.0.0.1:41000/"
}

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
			if(resp.json()[microS] != None):
				message = {
				'status_code': 200,
				'message': 'OK',
				str(microS): resp.json()[microS]
				}
			else:
				message = {
				'status_code': 200,
				'message': 'Resource not found at microservice',
				str(microS): None
				}
	except:
		message = {
			'status_code': 404,
			'message': 'Unable to perform API request to ' + str(microS) + ' microservice.',
			str(microS): None
		}
	return message

app = Flask(__name__)


# ERROR resource not found page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('serviceOfflineTemplate.html', type="found")





@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=302)

############ HTML #############
@app.route('/')
def homePage():
	return render_template("mainPage.html", services = microservices)

@app.route('/<path:subpath>')
def html(subpath):
	microS = subpath.split('/')[0]
	template = microS + "Template.html"
	response = API(subpath)
	json = response[microS]
	if json == None:
		return render_template("serviceOfflineTemplate.html", service="Secretariat", type="found")
	else:
		return render_template(template, microservice=microS, json=json)

# ########## REST API ###########

@app.route('/API/<path:subpath>')
def API(subpath):
	microS = subpath.split('/')[0]
	url = microservices[microS] + subpath

	message = API_microServices(url, microS)
	return message

if __name__ == '__main__':
	app.run(debug=True, port=39000)
