import os
from flask_cors import CORS
import urllib.request
from flask import Flask, request, redirect, jsonify, make_response, render_template
from werkzeug.utils import secure_filename
import cv2
import tensorflow as tf
import base64 
import numpy as np
import pdfkit

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, r'/templates')
app = Flask(__name__)
app.secret_key = "secret key"
CORS(app)
CATEGORIES = ['Negative','Positive']  # will use this to convert prediction num to string value
app.config['imgdir'] = '/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
model = tf.keras.models.load_model("COVID19-CNN.model")


def preprocess_img(img):
    IMG_SIZE = 225
    img_array = cv2.imdecode(img, cv2.IMREAD_COLOR)  # read in the image
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)  # return the image with shaping that TF wants.

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if not file:
            return "Missing file.", 400
        if not allowed_file(file.filename):
            return "Invalid file type.", 400
        print(f'file name: {file.filename}')
        img = np.fromfile(file, np.uint8)
        prediction = model.predict([preprocess_img(img)])
        category = CATEGORIES[int(prediction[0][0])]
        print("1")
        r = render_template('index.html', name = "Deema", result = category)
        config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
        print("1")
        pdf = pdfkit.from_string(r, False,  configuration=config)
        print(pdf)
        print(type(pdf))
        print("1")
        res = make_response(pdf)
        print("1")
        res.headers['Content-Type'] = 'application/pdf'
        res.headers['Content-Disposition'] = 'attachment; filename=result.pdf'
        return res, 200
    except Exception as e:
        print(e)
        return "MISSING_DATA", 400
    	# check if the post request has the file part


    
@app.route('/', methods=['GET'])
def welcome():
		return 'Welcome'

if __name__ == "__main__":
    app.run(port=4376, debug=False)