from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy 
# from flask_marshmallow import Marshmallow
from flask_mqtt import Mqtt
from sys import argv
import time
import db
from copy import deepcopy
import json
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensors_data.db' # new

app.config['MQTT_BROKER_URL'] = '192.168.1.110'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1884  # default port for non-tlp connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 20  # set the time interval for sending a ping to the broker to 20 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):

api_token = '6ytwk4ivTB7QkmlL0QPA1HNQ7NCOAb6Y'

try:
    mqtt = Mqtt(app)
    mqtt.subscribe('#')    
except:
    print('unable to start mqtt server')

