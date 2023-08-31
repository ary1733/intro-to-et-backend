from datetime import timedelta
from flask import Flask, jsonify, request
from flask_api import status
from os import environ, makedirs as os_makedirs, path as os_path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
# from flask_jwt_extended.exceptions import JWTExtendedException
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler

db = SQLAlchemy()
jwt = JWTManager()

def init_app():

	app = Flask(__name__)
	CORS(app,resources={r'*':{'origins':'*','supports_credentials':True}})

	# Configure the logger
	log_file_path = './logs/flask_app.log'
	os_makedirs(os_path.dirname(log_file_path), exist_ok=True)
	handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=5)
	formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	handler.setFormatter(formatter)
	app.logger.removeHandler(default_handler)
	app.logger.addHandler(handler)
	app.logger.setLevel(logging.INFO)
	@app.after_request
	def log_requests(response):
		app.logger.info('[' + request.method + '] ' +'[' + request.full_path + '] ' + '[' + response.status + '] ' + '[' + response.data.decode('utf-8').strip() + ']')
		return response
	
	# configure the environment variables
	load_dotenv()
	app.config['DEBUG'] = eval(environ["DEBUG_MODE"]) # Debug mode for flask app
	app.config['SQLALCHEMY_DATABASE_URI'] = environ["SQL_URL"] # connection string for postgres sql database
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # set it to False to disable tracking and use less memory
	app.config['JWT_SECRET_KEY'] = environ["JWT_SECRET"] # secret key for JWT
	# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=10)
	app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
	app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
	app.config["JWT_ERROR_MESSAGE_KEY"] = 'message'
	app.config['TRAP_HTTP_EXCEPTIONS']=True
	print('\tFlask App configurations loaded...')

	# Error handler
	@app.errorhandler(Exception)
	def handle_error(e):
		return jsonify({'message': str(e)}), status.HTTP_500_INTERNAL_SERVER_ERROR

	db.init_app(app)
	print('\tDatabase initialised...')
	jwt.init_app(app)
	print('\tJWT initialised...')

	# first register the blue prints which
	# will initialise the db models like
	# user,post etc.
	from src.user import user_blueprint
	from src.post import post_blueprint
	from src.category import category_blueprint
	for blueprint in [user_blueprint,post_blueprint,category_blueprint]:
		print('\troutes for '+str(blueprint)+' loaded...')
		app.register_blueprint(blueprint)

	# now create tables for the initialised
	# db models
	with app.app_context():
		db.create_all()
	print('\tDatabase tables created...')

	with app.app_context():
		from src.category.model import Category
		file = open('./src/predict/labels.txt', 'r')
		for line in file.readlines():
			categoryName=line.strip()
			old_category = Category.query.filter_by(categoryName=categoryName).one_or_none()
			if(old_category): # if the ml trained category already present, dont add again in table
				continue
			new_category = Category(categoryName=categoryName,isTrained=True)
			db.session.add(new_category)
			print('\tML trained category '+categoryName+' added in session...')
		db.session.commit()
		print('\tAll ML trained categories commited successfully...')

	print('\tFlask App created successfully...')
	return app