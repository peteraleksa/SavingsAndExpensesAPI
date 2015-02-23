#!flask/bin/python

from flask import Flask, jsonify, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://savings:expenses@localhost/savings_and_expenses'


#
# Relationship Tables:
#

user_teams = db.Table('user_team',
	db.Column('team_id', db.Integer, db.ForeignKey('team._id')),
	db.Column('user_id', db.Integer, db.ForeignKey('user._id'))
)

user_goals = db.Table('user_goal',
	db.Column('user_id', db.Integer, db.ForeignKey('user._id')),
	db.Column('goal_id', db.Integer, db.ForeignKey('goal._id'))
)

user_goal_schedules = db.Table('user_goal_schedule',
	db.Column('user_id', db.Integer, db.ForeignKey('user._id')),
	db.Column('goal_schedule_id', db.Integer, db.ForeignKey('goal_schedule._id'))
)

user_deposits = db.Table('user_deposit',
	db.Column('user_id', db.Integer, db.ForeignKey('user._id')),
	db.Column('deposit_id', db.Integer, db.ForeignKey('deposit._id'))
)

team_goals = db.Table('team_goal',
	db.Column('team_id', db.Integer, db.ForeignKey('team._id')),
	db.Column('goal_id', db.Integer, db.ForeignKey('goal._id'))
)

team_expenses = db.Table('team_expense',
	db.Column('team_id', db.Integer, db.ForeignKey('team._id')),
	db.Column('expense_id', db.Integer, db.ForeignKey('expense._id'))
)


#
# Models:
#

class User(db.Model):
	__tablename__ = 'user'
	_id = db.Column(db.Integer, primary_key = True, nullable=False)
	name = db.Column(db.String(25), nullable=False)
	email = db.Column(db.String(50), nullable=True)
	password = db.Column(db.String(25), nullable=False)
	teams = db.relationship('Team', secondary=user_teams,
		backref=db.backref('team', lazy='dynamic'))
	goals = db.relationship('Goal', secondary=user_goals,
		backref=db.backref('user', lazy='dynamic'))

class Team(db.Model):
	__tablename__ = 'team'
	_id = db.Column(db.Integer, primary_key = True, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(250), nullable=True)
	users = db.relationship('User', secondary=user_teams,
		backref=db.backref('user', lazy='dynamic'))

class Expense(db.Model):
	__tablename__ = 'expense'
	_id = db.Column(db.Integer, primary_key = True, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(250), nullable=True)
	amount = db.Column(db.Float(10, 2), nullable=False)
	recurring = db.Column(db.Boolean, nullable=False)
	frequency = db.Column(db.Integer, nullable=True)

class Goal(db.Model):
	__tablename__ = 'goal'
	_id = db.Column(db.Integer, primary_key = True, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(250), nullable=True)
	amount = db.Column(db.Float(10, 2), nullable=False)
	start_date = db.Column(db.Date, nullable=False)
	target_date = db.Column(db.Date, nullable=False)
	end_date = db.Column(db.Date, nullable=False)
	priority = db.Column(db.Integer, nullable=False)
	users = db.relationship('User', secondary=user_goals,
		backref=db.backref('goal', lazy='dynamic'))

class Schedule(db.Model):
	__tablename__ = 'goal_schedule'
	_id = db.Column(db.Integer, primary_key=True, nullable=False)
	goal_id = db.Column(db.Integer, db.ForeignKey('goal._id'))
	frequency = db.Column(db.Integer, nullable=False)
	amount = db.Column(db.Float, nullable=False)

class Deposit(db.Model):
	__tablename__ = 'deposit'
	_id = db.Column(db.Integer, primary_key=True, nullable=False)
	dep_date = db.Column(db.Date, nullable=False)
	amount = db.Column(db.Float, nullable=False)
	verified = db.Column(db.Boolean, nullable=False)
	allocations = db.relationship('Allocation', backref='deposit', lazy='dynamic')

class Allocation(db.Model):
	__tablename__ = 'deposit_allocation'
	_id = db.Column(db.Integer, primary_key=True, nullable=False)
	deposit_id = db.Column(db.Integer, db.ForeignKey('deposit._id'))
	percentage = db.Column(db.Integer, nullable=False)


#
# Routes:
#

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
	user = {
		'name': request.json['name'],
		'email': request.json.get('email', ""),
		'password': request.json['password']
	}

	# add to dbase
	#

	return jsonify({'user': user}), 201

@app.route('/expsav/api/v1.0/teams', methods=['POST'])
@auth.login_required
def create_team():
	if not request.json or not 'name' in request.json:
		abort(400)

	team = Team(name=request.json['name'],
				description=request.json.get('description', "")
			)
	#team = {
	#	'name': request.json['name'],
	#	'description' = request.json.get('description', "")
	#}

	# add to db
	db.session.add(team)
	db.session.commit()

	return jsonify({'team': team}), 201

if __name__ == '__main__':
	app.run(debug=True)