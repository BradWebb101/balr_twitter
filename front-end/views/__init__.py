from flask import render_template, request, redirect, url_for, session
from app import app
from model import *
from helpers import get_data_dict

@app.route('/', methods=["GET"])
def home():
        data_dict = get_data_dict.get_data_dict().data_dict
        return render_template('index.html', data=data_dict)

#404 Page
@app.route('/404', methods=["GET"])
def errorpage():
    return render_template("404.html")

