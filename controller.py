from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
from sys import argv
import time
import db
from copy import deepcopy
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from matplotlib.pyplot import figure, close
import atexit
from AutoML.AutoML import AutoTuningHyperparameters, DataPreprocessor
from Clustering import K_MEAN
from requests import get
import pickle
import io


from sklearn.metrics import fbeta_score, balanced_accuracy_score

def f1_score(y_true, y_pred, threshold = 0.5):
    y_pred_class = y_pred >= threshold
    y_true = y_true == 1
    return fbeta_score(y_true, y_pred_class, beta = 1)


api_token = '6ytwk4ivTB7QkmlL0QPA1HNQ7NCOAb6Y'


