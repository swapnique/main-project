# from __future__ import division, print_function

from flask import Flask,render_template
import pickle
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from flask import request

import sys
import os
import glob
import re
import numpy as np
import cv2
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import  redirect, url_for, request
#from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app=Flask(__name__)

MODEL_PATH = 'git_model.h5'


model = load_model(MODEL_PATH)

print('Model loaded. Start serving...')

print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):

    
    img = cv2.imread(img_path)
    new_arr = cv2.resize(img, (100, 100))
    new_arr = np.array(new_arr/255)
    new_arr = new_arr.reshape(-1, 100, 100, 3)

    preds = model.predict(new_arr)
    return preds


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crop.html')
def crop():
    return render_template('crop.html')

@app.route('/fertilizer.html')
def fertilizer():
    return render_template('fertilizer.html')


@app.route('/yield.html')
def yie():
    return render_template('yield.html') 


@app.route('/disease.html', methods=['GET'])
def disease():
    return render_template('disease.html')

@app.route('/pesticide.html')
def pesticide():
    return render_template('pesticide.html')


@app.route('/submit2',methods=['POST'])
def submit2():
    if request.method == 'POST':

        temparature=request.form['temparature'].strip()
        humidity=request.form['humidity'].strip()
        moisture=request.form['moisture'].strip()
        
        soiltypes=request.form['soilvalue'].strip()
        
        croptypes=request.form['cropvalue'].strip()
        print(soiltypes)
        print(croptypes)
        nitrogen=request.form['nitrogen'].strip()
        phosphorous=request.form['phosphorous'].strip()
        potassium=request.form['potassium'].strip()
        data=[[float(temparature),float(humidity),float(moisture),float(soiltypes),float(croptypes),float(nitrogen),float(potassium),float(phosphorous)]]
        print(data)
        lr=pickle.load(open('xgb.pkl','rb'))
        pr=lr.predict(data)
        print("value",pr)
    
        if pr==0:
            output="10-26-26"
        elif pr==1:
            output="14-35-14"
        elif pr==2:
            output="17-17-17"
        elif pr==3:
            output="20-20"
        elif pr==4:
            output="28-28"
        elif pr==5:
            output="DAP"
        else:
            output="Urea"


    return render_template('fertilizer.html',prediction=output)




@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':

        nitrogen=request.form['nitrogen']
        phosphorous=request.form['phosphorous']
        potassium=request.form['potassium']
        temperature=request.form['temperature']
        humidity=request.form['humidity']
        ph=request.form['ph']
        rainfall=request.form['rainfall']

        data=[[float(nitrogen),float(phosphorous),float(potassium),float(temperature),float(humidity),float(ph),float(rainfall)]]

        lr2=pickle.load(open('rfc.pkl','rb'))
        pred=lr2.predict(data)[0]

    return render_template('crop.html',prediction=pred)


@app.route('/submit3',methods=['POST'])
def submit3():
    if request.method=='POST':
        statename=request.form['statevalue']
        season=request.form['seasonvalue']
        crop=request.form['cropvalue']
        area=request.form['area']
        rainfall=request.form['rainfall']
        # data1=[[float(statename),float(cropyear),float(season),float(crop),float(area),float(rainfall)]]
        data1=[[float(statename),float(season),float(crop),float(area),float(rainfall)]]

  
        lr3=pickle.load(open('yieldcheck1.pkl','rb'))
        pred=lr3.predict(data1)[0]
    return render_template('yield.html',prediction=pred)



@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        f = request.files['file']

        
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', f.filename)  
        f.save(file_path)

        
        preds = model_predict(file_path, model)

        
        pred_class = preds.argmax()              

        CATEGORIES = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
                      'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                      'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
                      'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                      'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                      'Tomato__YellowLeaf__Curl_Virus', 'Tomato_mosaic_virus',
                      'Tomato_healthy']
        return CATEGORIES[pred_class]

        
    return None

if __name__=='__main__':
    app.run(debug = True)