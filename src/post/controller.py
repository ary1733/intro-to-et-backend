from flask import jsonify, request
from src import db
from sqlalchemy import text
from src.post import post_blueprint
from src.post.model import Post
from src.user.model import User
from flask_jwt_extended import (
	jwt_required,
	get_jwt_identity,
)

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


	if ((imgID==None) or (None==unixTime)):
		raise Exception('please provide all arguments')
	
	identity = get_jwt_identity()
	new_post = Post(description=description,imgID=imgID,unixTime=unixTime,userId=identity)
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
		select description,"imgID","unixTime",email,name, p.id as id
		from posts p inner join users u
		on p."userId" = u.id
		order by "unixTime" desc
		'''
		if(user.role=="USER"):
			query = f'''
			select description,"imgID","unixTime",email,name, p.id as id
			from posts p inner join users u
			on p."userId" = u.id
			where u.id = {userId}
			order by "unixTime" desc
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