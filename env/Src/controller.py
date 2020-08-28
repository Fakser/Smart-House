from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_mqtt import Mqtt
from sys import argv

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensors_data.db' # new

app.config['MQTT_BROKER_URL'] = '192.168.0.249'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1884  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

db = SQLAlchemy(app)
ma = Marshmallow(app)
mqtt = Mqtt(app)
# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
mqtt.subscribe('topic1')    
