#!flask/bin/python

from flask import Flask, jsonify, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'pete':
		return 'python'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

#@app.route('/expsav/api/v1.0/me', methods=['GET'])
#def get_my_profile():
#	return jsonify({'tasks': tasks})

@app.route('/expsav/api/v1.0/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
	# get user from db
	pass

@app.route('/expsav/api/v1.0/groups', methods=['GET'])
@auth.login_required
def get_groups():
	return jsonify({'groups': groups})

@app.route('/expsav/api/v1.0/groups/<int:group_id>', methods=['GET'])
@auth.login_required
def get_group(group_id):
	# get group from db
	group = [group for group in groups if group['_id'] == group_id]
	
	if len(group) == 0:
		abort(404)
	
	return jsonify({'group': group[0]})

@app.route('/expsav/api/v1.0/users', methods=['POST'])
@auth.login_required
def create_user():
	if not request.json or not 'name' in request.json or not 'password' in request.json:
		abort(400)
	user = {
		'name': request.json['name'],
		'email': request.json.get('email', ""),
		'password': request.json['password']
	}

	# add to dbase
	#

	return jsonify({'user': user}), 201

@app.route('expsav/api/v1.0/groups', methods=['POST'])
@auth.login_required
def create_group():
	if not request.json or not 'name' in request.json:
		abort(400)
	group = {
		'name': request.json['name'],
		'description' = request.json.get('description', "")
	}

	# add to db
	#

	return jsonify({'group': group}), 201

if __name__ == '__main__':
	app.run(debug=True)