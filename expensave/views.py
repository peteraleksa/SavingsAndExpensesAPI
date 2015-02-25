# views.py

from expensave import app
from flask import jsonify, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from expensave.models import User, Team, Expense, Goal, Schedule, Deposit, Allocation

from expensave.database import db_session

auth = HTTPBasicAuth()

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

def perform_login():
	pass

def show_login_form():
	pass

# Routes:

@auth.get_password
def get_password(username):
	if username == 'savings':
		return 'expenses'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		perform_login()
	else:
		show_login_form()

#@app.route('/expsav/api/v1.0/me', methods=['GET'])
#def get_my_profile():
#	return jsonify({'tasks': tasks})

@app.route('/expsav/api/v1.0/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
	# get user from db
	pass

@app.route('/expsav/api/v1.0/teams', methods=['GET'])
@auth.login_required
def get_teams():
	if request.method == 'GET':
		results = Team.query.limit(10).offset(0).all()

		json_results = []
		for result in results:
			t = {'_id': result._id,
				 'name': result.name,
				 'description': result.description,
				 'users': result.users
			}
			json_results.add(t)

	return jsonify({'teams': json_results})

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

	user = User(name=request.json['name'],
				password=request.json['password'],
				email=request.json.get('email', ""))

	user.save()

	user_dict = {
		'name': user.name,
		'email': user.email,
		'password': user.password
	}

	return jsonify({'user': user_dict}), 201

@app.route('/expsav/api/v1.0/teams', methods=['POST'])
@auth.login_required
def create_team():
	if not request.json or not 'name' in request.json:
		abort(400)

	team = Team(name=request.json['name'],
				description=request.json.get('description', "")
			)

	team.save()

	team_dict = {
		'id': team._id,
		'name': team.name,
		'description': team.description
	}


	return jsonify({'team': team_dict}), 201