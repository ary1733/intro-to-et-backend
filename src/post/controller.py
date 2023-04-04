from flask import jsonify, request
from src import db
from sqlalchemy import text
from src.post import post_blueprint
from src.post.model import Post
from src.user.model import User
from src.category.model import Category
from google.cloud import storage
from flask_jwt_extended import (
	jwt_required,
	get_jwt_identity,
)
import uuid

@post_blueprint.post('/uploadPostImage')
@jwt_required()
def uploadPostImage():
	file = request.files.get('file')
	if file is None or file.filename == "":
		return jsonify({'success': False,"message": "no file"})
	try:
		
		storage_client = storage.Client.from_service_account_json('credentials.json')
		bucket = storage_client.get_bucket('post-images-btp-backend')
		blob = bucket.blob(str(uuid.uuid4()))
		blob.upload_from_file(file,content_type=file.content_type)
		return jsonify({'success': True,"public_url": blob.public_url})
	
	except Exception as e:
		
		return jsonify({'success': False,"message": str(e)})

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
		return jsonify({'success': False, 'message': 'please provide all arguments'})
	
	try:
		category = Category.query.filter_by(id=categoryId).one_or_none()
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})
	
	if (not category):
		return jsonify({'success': False, 'message': 'no category found with categoryId=[{}]'.format(categoryId)})
	
	identity = get_jwt_identity()

	new_post = Post(description=description,imgLink=imgLink,unixTime=unixTime,longitude=longitude,latitude=latitude,userId=identity,categoryId=categoryId)
	try:
		db.session.add(new_post)
		db.session.commit()
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})

	return jsonify({'success': True, 'message': 'Post created successfully'})

@post_blueprint.get('/allPosts')
@jwt_required()
def allPosts():
	try:
		lst=[]
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			return jsonify({'success': False, 'message': 'user with id=[{}] not present.'.format(userId)})
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
		return jsonify({'success': False, 'message': str(e)})
	return jsonify({'success': True,'list':lst})

@post_blueprint.get('/getPost/<int:post_id>')
@jwt_required()
def getPost(post_id):
	try:
		post = Post.query.filter_by(id=post_id).one_or_none()
		if (not post):
			return jsonify({'success': False, 'message': 'post with id=[{}] not present.'.format(post_id)})
		
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			return jsonify({'success': False, 'message': 'user with id=[{}] not present.'.format(userId)})
		if(user.role=="USER" and userId!=post.userId):
			return jsonify({'success': False, 'message': 'user with id=[{}] is not the author for post with id=[{}].'.format(userId,post_id)})
		
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})
	return jsonify({'success': True, 'post': post.as_dict()})

@post_blueprint.delete('/deletePost/<int:post_id>')
@jwt_required()
def deletePost(post_id):
	try:
		post = Post.query.filter_by(id=post_id).one_or_none()
		if (not post):
			return jsonify({'success': False, 'message': 'post with id=[{}] not present.'.format(post_id)})
		
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			return jsonify({'success': False, 'message': 'user with id=[{}] not present.'.format(userId)})
		if(user.role=="USER" and userId!=post.userId):
			return jsonify({'success': False, 'message': 'user with id=[{}] is not the author for post with id=[{}].'.format(userId,post_id)})

		db.session.delete(post)
		db.session.commit()
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})
	return jsonify({'success': True, 'message': 'post with id=[{}] deleted successfully.'.format(post_id)})