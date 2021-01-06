from flask import render_template, request, redirect, url_for, session
from app import app
from model import *
from helpers import get_data_dict
from flask import jsonify
import json

@app.route('/', methods=["GET"])
def home():
        data_dict = get_data_dict.get_data_dict().data
        if data_dict:
                return render_template('favourites.html', data=data_dict)
        else:
            return render_template("404.html")  

@app.route('/favourites', methods=["GET"])
def favourites():
        data_dict = get_data_dict.get_data_dict().data
        if data_dict:
                return render_template('favourites.html', data=data_dict)
        else:
            return render_template("404.html")  
    
@app.route('/retweets', methods=["GET"])
def retweets():
        data_dict = get_data_dict.get_data_dict().data
        if data_dict:
                return render_template('retweets.html', data=data_dict)
        else:
            return render_template("404.html")  