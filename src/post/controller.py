from flask import jsonify, request, send_file,current_app
from src import db
from sqlalchemy import text
from src.post import post_blueprint
from src.post.model import Post
from src.user.model import User
from src.category.model import Category
from flask_jwt_extended import (
	jwt_required,
	get_jwt_identity,
)
import uuid
import os
from pathlib import Path
from werkzeug.utils import secure_filename

@post_blueprint.get('/getPostImage/<string:file_name>')
# @jwt_required(), currently the image links are public
def getPostImage(file_name):
	directory = os.path.join(Path.cwd(),current_app.config['IMG_UPLOAD_FOLDER'])
	existing_file_path = os.path.join(directory, file_name)
	return send_file(existing_file_path, as_attachment=False)

@post_blueprint.post('/uploadPostImage')
@jwt_required()
def uploadPostImage():
	file = request.files.get('file')
	if file is None or file.filename == "":
		raise Exception('no file provided')

	directory = os.path.join(Path.cwd(),current_app.config['IMG_UPLOAD_FOLDER'])
	file_name = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
	saved_file_path = os.path.join(directory,file_name )
	file.save(saved_file_path)
	return jsonify({"imgID": file_name})

@post_blueprint.get('/ping')
@jwt_required()
def ping():
	return jsonify('OK')

@post_blueprint.post('/createPost')
@jwt_required()
def createPost():
	description = request.json.get("description")
	imgID = request.json.get("imgID")
	unixTime = request.json.get("unixTime")
	longitude = request.json.get("longitude")
	latitude = request.json.get("latitude")
	categoryId = request.json.get("categoryId")

	if ((imgID==None) or (None==unixTime) or (None==longitude) or (None==latitude) or (None==categoryId)):
		raise Exception('please provide all arguments')
	
	try:
		category = Category.query.filter_by(id=categoryId).one_or_none()
	except Exception as e:
		raise e
	
	if (not category):
		raise Exception('no category found with categoryId=[{}]'.format(categoryId))
	
	identity = get_jwt_identity()

	new_post = Post(description=description,imgID=imgID,unixTime=unixTime,longitude=longitude,latitude=latitude,userId=identity,categoryId=categoryId)
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
		select description,imgID,unixTime,longitude,latitude,categoryName,email, p.id as id
		from posts p inner join users u
		on p.userId = u.id
		inner join categories c on p.categoryId = c.id
		order by unixTime desc
		'''
		if(user.role=="USER"):
			query = f'''
			select description,imgID,unixTime,longitude,latitude,categoryName,email, p.id as id
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