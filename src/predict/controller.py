from flask import jsonify, request
from src import db
from src.predict import predict_blueprint
from flask_jwt_extended import jwt_required
from src.predict import transform,batch_size,device,model,labels_map

import torch
from PIL import Image
import io

@predict_blueprint.get('/ping')
@jwt_required()
def ping():
    return jsonify('OK')

def batch_from_image(img):
	
	image = transform(img) # transform image, dimesnion of image=3x640x640 
	"""
	Now, we got just 1 one image of dimension 3x640x640 (3D tensor)
	However, we have trained our model to give predictions
	for a batch of images with batch size = batch_size
	So, we make a 4D tensor, in which we just make the copy of
	image batch_size times
	"""
	images = image[None] # add 1 dimension, dimesnion of images=1x3x640x640 
	lst = []
	for i in range(batch_size):
		lst.append(images)
	images = torch.cat(lst) #dimesnion of images=4x3x640x640
	images = images.to(device)
	return images

@predict_blueprint.post('/predict')
@jwt_required()
def predict():
	file = request.files.get('file')
	if file is None or file.filename == "":
		return jsonify({'success': False,"message": "no file"})
	try:
		image_bytes = file.read()
		
		pillow_img = Image.open(io.BytesIO(image_bytes))
		images = batch_from_image(pillow_img)
		outputs = model(images)
		"""
		dimension of outputs is
		batch_size x no_of_classes 
		"""
		output = outputs[0] # get the first item from batch
		_, predicted = torch.sort(output,descending=True)
		lst = []
		for i in range(len(predicted)):
			lst.append(labels_map[str(int(predicted[i]))])
		return jsonify({'success': True,"prediction" : lst})
	except Exception as e:
		return jsonify({'success': False,"message": str(e)})