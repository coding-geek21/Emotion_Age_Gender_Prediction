from flask import Blueprint, render_template, request, flash, jsonify
from flask import Flask, redirect, url_for
from werkzeug.utils import secure_filename
import json
from flask.helpers import flash
import cv2

# import modules for Prediction
import os
import numpy as np
from joblib import Parallel, delayed
import joblib

MODEL_PATH ='emotion_model.pkl'

views = Blueprint('views', __name__)

model = joblib.load(MODEL_PATH)
model1 = joblib.load('age.pkl')
model2 = joblib.load('filename.pkl')

dec = {0:'anger', 1:'contempt', 2:'disgust', 3:'fear', 4:'happy', 5:'sadness', 6:'surprise'}
gen = {0:'male', 1:'female'}

def predict_model(img_path, model,img_file):
    print(img_path)
    img = cv2.imread(img_path,0)
    img1 = cv2.resize(img, (200,200))
    img1 = img1.reshape(1,-1)/255
  
    res=[]
    preds = model.predict(img1)
    preds=dec[preds[0]]   
    preds1= model1.predict(img1) 
    preds2= model2.predict(img1)
    if preds2==0:
        preds2="male"
    else:
        preds2="female"
    res.append(preds)
    res.append(preds1)
    res.append(preds2)
    return res
    full_filename = path.join(app.config['UPLOAD_FOLDER'], img_file)
    print(full_filename)
    return render_template("predict.html", user_image = full_filename)

@views.route('/predict', methods=['GET', 'POST'])
def make_prediction():
    result = 0
    age = 0
    gender = 0
    if request.method == 'POST':
        f = request.files['face-img']

        if f.filename == "":
            flash("Please select a proper image!", category="error")
            pass

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'static\img-uploads', secure_filename(f.filename))
        f.save(file_path)

        preds = predict_model(file_path,model,secure_filename(f.filename))
        print(preds)
        result = preds[0]
        age = preds[1]
        gender = preds[2]
    return render_template('predict.html', prediction_result=result, age_val=age, gender_val=gender)