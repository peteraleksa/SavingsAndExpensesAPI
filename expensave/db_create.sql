CREATE DATABASE savings_and_expenses;
USE savings_and_expenses;


CREATE TABLE user (

	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(25) NOT NULL,
	email VARCHAR(50),
	password VARCHAR(25) NOT NULL

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE team (

	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	description VARCHAR(250)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE expense (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	description VARCHAR(250),
	amount FLOAT(10, 2) NOT NULL,
	recurring BOOL NOT NULL,
	frequency INT

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE goal (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	description VARCHAR(250),
	amount FLOAT(10, 2) NOT NULL,
	start_date DATE NOT NULL,
	target_date DATE NOT NULL,
	end_date DATE NOT NULL,
	priority INT NOT NULL

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE goal_schedule (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	goal_id INT NOT NULL,
	frequency INT NOT NULL,
	amount DOUBLE(10, 2) NOT NULL,

	INDEX (goal_id),

	FOREIGN KEY (goal_id)
		REFERENCES goal(_id)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE deposit (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	dep_date DATE NOT NULL,
	amount DOUBLE(10,2) NOT NULL,
	verified BOOL NOT NULL

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE deposit_allocation (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	deposit_id INT NOT NULL,
	goal_id INT NOT NULL,
	percentage INT NOT NULL,

	INDEX (deposit_id),
	INDEX (goal_id),

	FOREIGN KEY (deposit_id)
		REFERENCES deposit(_id),
	FOREIGN KEY (goal_id)
		REFERENCES goal(_id)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE user_team (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	team_id INT NOT NULL,

	INDEX (user_id),
	INDEX (team_id),

	FOREIGN KEY (user_id)
		REFERENCES user(_id),
	FOREIGN KEY (team_id)
		REFERENCES team(_id)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE user_goal (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	goal_id INT NOT NULL,

	INDEX(user_id),
	INDEX(goal_id),

	FOREIGN KEY (user_id)
		REFERENCES user(_id),
	FOREIGN KEY (goal_id)
		REFERENCES goal(_id)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE user_goal_schedule (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	goal_sched_id INT NOT NULL,

	INDEX (user_id),
	INDEX (goal_sched_id),

	FOREIGN KEY (user_id)
		REFERENCES user(_id),
	FOREIGN KEY (goal_sched_id)
		REFERENCES goal_schedule(_id)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE user_deposit (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	deposit_id INT NOT NULL,

	INDEX (user_id),
	INDEX (deposit_id),

	FOREIGN KEY (user_id)
		REFERENCES user(_id),
	FOREIGN KEY (deposit_id)
		REFERENCES deposit(_id)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE team_goal (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	team_id INT NOT NULL,
	goal_id INT NOT NULL,

	INDEX (team_id),
	INDEX (goal_id),

	FOREIGN KEY (team_id)
		REFERENCES team(_id),
	FOREIGN KEY (goal_id)
		REFERENCES goal(_id)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE team_expense (
	
	_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	team_id INT NOT NULL,
	expense_id INT NOT NULL,

	INDEX (team_id),
	INDEX (expense_id),

	FOREIGN KEY (team_id)
		REFERENCES team(_id),
	FOREIGN KEY (expense_id)
		REFERENCES expense(_id)

) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;

GRANT all ON savings_and_expenses.* to 'savings'@localhost;
