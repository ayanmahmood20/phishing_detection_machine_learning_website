from app.api.mod import extract_website_features
from app.app_init import app
from flask import render_template ,request
import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import socket
import tldextract
import whois
from datetime import datetime
import numpy as np
from flask import Blueprint

api=Blueprint('api',__name__,template_folder='/home/ayanksi183/Documents/New_flask/app/templates')

@api.route('/')
def home():
    return render_template('src.html')

@api.route('/url')
def url():
    return render_template('index.html')
@api.route('/predict', methods=['POST'])
def predict():
    with open("/home/ayanksi183/Documents/New_flask/app/routes/XGBoostClassifier.pickle.dat","rb") as f:
        model=pickle.load(f)
    url = request.form['url']
    
    # Extract website features
    website_features = extract_website_features(url)
    preprocessed_data = {key: 1 if value is True else (0 if value is False else value) for key, value in website_features.items()}
   
    df = np.array(list(preprocessed_data.values()))
    # Make predictions using the loaded XGBoost model
    prediction = model.predict([df])
    proba = (model.predict_proba([df]))
    
    if prediction == 1:
        result = "Phished"
        proba_phished = round(proba[0][1]*100,2)
        proba_legit = round(proba[0][0]*100,2)
    else:
        result = "Legit"
        proba_phished = round(proba[0][1]*100,2)
        proba_legit = round(proba[0][0]*100,2)
    
    return render_template('result.html',url=url, result=result,proba_phished=proba_phished, proba_legit=proba_legit,df=df)