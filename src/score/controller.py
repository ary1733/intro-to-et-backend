from flask import jsonify, request
from src import db
from sqlalchemy import text
from src.score import post_blueprint
from src.score.model import Score
from src.user.model import User
from flask_jwt_extended import (
	jwt_required,
	get_jwt_identity,
)

@post_blueprint.get('/ping')
@jwt_required()
def ping():
	return jsonify('OK')

@post_blueprint.post('/submitScore')
@jwt_required()
def submitScore():
	level = request.json.get("level")
	timetaken = request.json.get("timetaken")
	# unixTime = request.json.get("unixTime")


	if ((level==None) or (None==timetaken)):
		raise Exception('please provide all arguments')
	
	identity = get_jwt_identity()
	new_post = Score(level=level,timetaken=timetaken,userId=identity)
	try:
		db.session.add(new_post)
		db.session.commit()
	except Exception as e:
		raise e

	return jsonify({'message': 'Post created successfully'})

@post_blueprint.get('/allscores')
@jwt_required()
def allscores():
	
	try:
		lst=[]
		userId = get_jwt_identity()
		user = User.query.filter_by(id=userId).one_or_none()
		if(not user):
			raise Exception('user with id=[{}] not present.'.format(userId))
		query = '''
		select level,timetaken,email,name, s.id as id
		from scores s inner join users u
		on s."userId" = u.id
		'''
		with db.engine.connect() as conn:
			lst = conn.execute(text(query))
			lst = lst.mappings().all()
			lst = [dict(row) for row in lst]
	except Exception as e:
		raise e
	# print(lst)
	leaderboard = {	}
	for row in lst:
		if row['email'] in leaderboard.keys():

			if(row['level'] > leaderboard[row['email']]['level']):
				leaderboard[row['email']] = row
			elif row['level'] == leaderboard[row['email']]['level']:
				if(row['timetaken'] < leaderboard[row['email']]['timetaken']):
					leaderboard[row['email']] = row
		else:
			leaderboard[row['email']] = row
			

	return jsonify({'list':list(leaderboard.values())})

# @post_blueprint.get('/getPost/<int:post_id>')
# @jwt_required()
# def getPost(post_id):
# 	try:
# 		post = Post.query.filter_by(id=post_id).one_or_none()
# 		if (not post):
# 			raise Exception('post with id=[{}] not present.'.format(post_id))
		
# 		userId = get_jwt_identity()
# 		user = User.query.filter_by(id=userId).one_or_none()
# 		if(not user):
# 			raise Exception('user with id=[{}] not present.'.format(userId))
# 		if(user.role=="USER" and userId!=post.userId):
# 			raise Exception('user with id=[{}] is not the author for post with id=[{}].'.format(userId,post_id))
		
# 	except Exception as e:
# 		raise e
# 	return jsonify({'success': True, 'post': post.as_dict()})

# @post_blueprint.delete('/deletePost/<int:post_id>')
# @jwt_required()
# def deletePost(post_id):
# 	try:
# 		post = Post.query.filter_by(id=post_id).one_or_none()
# 		if (not post):
# 			raise Exception('post with id=[{}] not present.'.format(post_id))
		
# 		userId = get_jwt_identity()
# 		user = User.query.filter_by(id=userId).one_or_none()
# 		if(not user):
# 			raise Exception('user with id=[{}] not present.'.format(userId))
# 		if(user.role=="USER" and userId!=post.userId):
# 			raise Exception('user with id=[{}] is not the author for post with id=[{}].'.format(userId,post_id))

# 		db.session.delete(post)
# 		db.session.commit()
# 	except Exception as e:
# 		raise e
# 	return jsonify({'success': True, 'message': 'post with id=[{}] deleted successfully.'.format(post_id)})