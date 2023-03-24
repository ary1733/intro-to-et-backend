from flask import jsonify, request
from src import db
from src.category import category_blueprint
from src.category.model import Category
from flask_jwt_extended import jwt_required

@category_blueprint.get('/ping')
@jwt_required()
def ping():
    return jsonify('OK')

@category_blueprint.post('/createCategory')
@jwt_required()
def createcategory():
    categoryName = request.json.get("categoryName")

    if (categoryName==None):
        return jsonify({'success': False, 'message': 'please provide all arguments'})
    

    new_category = Category(categoryName=categoryName,isTrained=False)
    try:
        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    return jsonify({'success': True, 'message': 'category created successfully'})

@category_blueprint.get('/allCategories')
@jwt_required()
def allCategories():
    try:
        lst = Category.query.all()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    return jsonify({'success': True, 'list': [obj.as_dict() for obj in lst]})

@category_blueprint.get('/getCategory/<int:categoryId>')
@jwt_required()
def getCategory(categoryId):
    try:
        category = Category.query.filter_by(id=categoryId).one_or_none()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    if (not category):
        return jsonify({'success': False, 'message': 'category with categoryId=[{}] not present.'.format(categoryId)})
    return jsonify({'success': True, 'category': category.as_dict()})