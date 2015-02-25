# models.py
import datetime

from expensave import app
from flask.ext.sqlalchemy import SQLAlchemy

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
	name = db.Column(db.String(25), nullable=False, unique=True)
	email = db.Column(db.String(50), nullable=True, unique=True)
	password = db.Column(db.String(25), nullable=False)
	teams = db.relationship('Team', secondary=user_teams,
		backref=db.backref('team', lazy='dynamic'))
	goals = db.relationship('Goal', secondary=user_goals,
		backref=db.backref('user', lazy='dynamic'))

	def __init__(self, name=None, password=None, email=None):
		self.name = name
		self.email = email
		self.password = password

	def save(self):
		db.session.add(self)
		db.session.commit()

class Team(db.Model):
	__tablename__ = 'team'
	_id = db.Column(db.Integer, primary_key = True, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(250), nullable=True)
	users = db.relationship('User', secondary=user_teams,
		backref=db.backref('user', lazy='dynamic'))

	def __init__(self, name=None, description=None):
		self.name = name
		self.description = description

	def save(self):
		db.session.add(self)
		db.session.commit()

class Expense(db.Model):
	__tablename__ = 'expense'
	_id = db.Column(db.Integer, primary_key = True, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	amount = db.Column(db.Float(10, 2), nullable=False)
	recurring = db.Column(db.Boolean, nullable=False)
	frequency = db.Column(db.Integer, nullable=True)
	description = db.Column(db.String(250), nullable=True)

	def __init__(self, name=None, amount=None, recurring=False, frequency=None, description=None):
		self.name = name
		self.amount = amount
		self.recurring = recurring
		self.frequency = frequency
		self.description = description

	def save(self):
		db.session.add(self)
		db.session.commit()

class Goal(db.Model):
	__tablename__ = 'goal'
	_id = db.Column(db.Integer, primary_key = True, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	amount = db.Column(db.Float(10, 2), nullable=False)
	start_date = db.Column(db.Date, nullable=False)
	target_date = db.Column(db.Date, nullable=False)
	end_date = db.Column(db.Date, nullable=False)
	priority = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String(250), nullable=True)
	users = db.relationship('User', secondary=user_goals,
		backref=db.backref('goal', lazy='dynamic'))

	def __init__(self, name=None, amount=None, start_date=datetime.datetime.now(), target_date=None, end_date=None, priority=None, description=None):
		self.name = name
		self.amount = amount
		self.start_date = start_date
		self.target_date = target_date
		self.end_date = end_date
		self.priority = priority
		self.description = description

	def save(self):
		db.session.add(self)
		db.session.commit()

class Schedule(db.Model):
	__tablename__ = 'goal_schedule'
	_id = db.Column(db.Integer, primary_key=True, nullable=False)
	goal_id = db.Column(db.Integer, db.ForeignKey('goal._id'))
	frequency = db.Column(db.Integer, nullable=False)
	amount = db.Column(db.Float, nullable=False)

	def __init__(self, goal_id=None, frequency=None, amount=None):
		self.goal_id = goal_id
		self.frequency = frequency
		self.amount = amount

	def save(self):
		db.session.add(self)
		db.session.commit()

class Deposit(db.Model):
	__tablename__ = 'deposit'
	_id = db.Column(db.Integer, primary_key=True, nullable=False)
	amount = db.Column(db.Float, nullable=False)
	dep_date = db.Column(db.Date, nullable=False)
	verified = db.Column(db.Boolean, nullable=False)
	allocations = db.relationship('Allocation', backref='deposit', lazy='dynamic')

	def __init__(self, amount=None, dep_date=datetime.datetime.now(), verified=False):
		self.amount = amount
		self.dep_date = dep_date
		self.verified = verified

	def save(self):
		db.session.add(self)
		db.session.commit()

class Allocation(db.Model):
	__tablename__ = 'deposit_allocation'
	_id = db.Column(db.Integer, primary_key=True, nullable=False)
	deposit_id = db.Column(db.Integer, db.ForeignKey('deposit._id'))
	percentage = db.Column(db.Integer, nullable=False)

	def __init__(self, deposit_id=None, percentage=None):
		self.deposit_id = deposit_id
		self.percentage = percentage

	def save(self):
		db.session.add(self)
		db.session.commit()

