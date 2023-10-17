from flask import jsonify, request, send_file, send_from_directory, Response,current_app
from src import db
from sqlalchemy import text
from src.post import post_blueprint
from src.post.model import Post
from src.user.model import User
from src.category.model import Category
# from google.cloud import storage
from flask_jwt_extended import (
	jwt_required,
	get_jwt_identity,
)
import uuid
from werkzeug.utils import secure_filename
import os
from pathlib import Path

@post_blueprint.get('/getPostImage/<string:file_name>')
@jwt_required()
def getPostImage(file_name):
	identity = get_jwt_identity()
	if(not identity):
		raise Exception('Invalid token')
	directory = os.path.join(Path.cwd(),'file_data',str(identity))
	existing_file_path = os.path.join(directory, file_name)
	print(existing_file_path)
	existing_file_path = '/Users/aryan/Desktop/btp-backend-flask/file_data/1/a.png'
	existing_file_path = '/Users/aryan/Desktop/btp-backend-flask/a.png'
	existing_file_path = '/Users/aryan/Desktop/btp-backend-flask/src/a.png'
	print(current_app.config['UPLOAD_FOLDER'])
	return send_file("/Users/aryan/Desktop/a.png", as_attachment=False)
	try:
		
		return send_file("/Users/aryan/Desktop/untitled-app/a.png", as_attachment=False)
	except Exception as e:
		print(e)

@post_blueprint.post('/uploadPostImage')
@jwt_required()
def uploadPostImage():
	file = request.files.get('file')
	if file is None or file.filename == "":
		raise Exception('no file provided')
	identity = get_jwt_identity()
	if(not identity):
		raise Exception('Invalid token')

	directory = os.path.join(Path.cwd(),'file_data',str(identity))
	Path(directory).mkdir(parents=True, exist_ok=True)
	file_name = secure_filename(file.filename)
	saved_file_path = os.path.join(directory,file_name )
	print(saved_file_path)
	file.save(saved_file_path)

	return jsonify({"public_url": file_name})


@post_blueprint.get('/ping')
@jwt_required()
def ping():
	return jsonify('OK')

@post_blueprint.post('/createPost')
@jwt_required()
def createPost():
	description = request.json.get("description")
	imgLink = request.json.get("imgLink")
	unixTime = request.json.get("unixTime")
	longitude = request.json.get("longitude")
	latitude = request.json.get("latitude")
	categoryId = request.json.get("categoryId")

	if ((imgLink==None) or (None==unixTime) or (None==longitude) or (None==latitude) or (None==categoryId)):
		raise Exception('please provide all arguments')
	
	try:
		category = Category.query.filter_by(id=categoryId).one_or_none()
	except Exception as e:
		raise e
	
	if (not category):
		raise Exception('no category found with categoryId=[{}]'.format(categoryId))
	
	identity = get_jwt_identity()

	new_post = Post(description=description,imgLink=imgLink,unixTime=unixTime,longitude=longitude,latitude=latitude,userId=identity,categoryId=categoryId)
	try:
		db.session.add(new_post)
		db.session.commit()
	except Exception as e:
		raise e

	return jsonify({'message': 'Post created successfully'})

@post_blueprint.get('/allPosts')
@jwt_required()
def allPosts():
	try:
		lst=[]
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			raise Exception('user with id=[{}] not present.'.format(userId))
		query = '''
		select description,imgLink,unixTime,longitude,latitude,categoryName,email, p.id as id
		from posts p inner join users u
		on p.userId = u.id
		inner join categories c on p.categoryId = c.id
		order by unixTime desc
		'''
		if(user.role=="USER"):
			query = f'''
			select description,imgLink,unixTime,longitude,latitude,categoryName,email, p.id as id
			from posts p inner join users u
			on p.userId = u.id
			inner join categories c on p.categoryId = c.id
			where u.id = {userId}
			order by unixTime desc
			'''
		with db.engine.connect() as conn:
			lst = conn.execute(text(query))
			lst = lst.mappings().all()
			lst = [dict(row) for row in lst]
	except Exception as e:
		raise e
	return jsonify({'list':lst})

@post_blueprint.get('/getPost/<int:post_id>')
@jwt_required()
def getPost(post_id):
	try:
		post = Post.query.filter_by(id=post_id).one_or_none()
		if (not post):
			raise Exception('post with id=[{}] not present.'.format(post_id))
		
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			raise Exception('user with id=[{}] not present.'.format(userId))
		if(user.role=="USER" and userId!=post.userId):
			raise Exception('user with id=[{}] is not the author for post with id=[{}].'.format(userId,post_id))
		
	except Exception as e:
		raise e
	return jsonify({'success': True, 'post': post.as_dict()})

@post_blueprint.delete('/deletePost/<int:post_id>')
@jwt_required()
def deletePost(post_id):
	try:
		post = Post.query.filter_by(id=post_id).one_or_none()
		if (not post):
			raise Exception('post with id=[{}] not present.'.format(post_id))
		
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			raise Exception('user with id=[{}] not present.'.format(userId))
		if(user.role=="USER" and userId!=post.userId):
			raise Exception('user with id=[{}] is not the author for post with id=[{}].'.format(userId,post_id))

		db.session.delete(post)
		db.session.commit()
	except Exception as e:
		raise e
	return jsonify({'success': True, 'message': 'post with id=[{}] deleted successfully.'.format(post_id)})