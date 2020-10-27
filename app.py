try:    
    from Src.controller import *
except:
    from controller import *

# app and scheduler
app = Flask(__name__)

cron = BackgroundScheduler(daemon=True)
cron.start()

app.config['MQTT_BROKER_URL'] = '192.168.1.110'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1884  # default port for non-tlp connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 20  # set the time interval for sending a ping to the broker to 20 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

#loading ml models
try:
    with open('./models/devices_rules', 'rb') as devices_rules_file:
        ml_models = pickle.load(devices_rules_file)
except:
    ml_models = {}
XGB_PARAMS = {'n_estimators ': [20, 300, 20], 
                'learning_rate': [0.01, 0.1, 0.01], 
                'max_depth': [3, 300, 30], 
                'subsample': [0.8, 1, 0.05], 
                'colsample_bytree': [0.3, 0.8, 0.05],
                'gamma': [0, 5, 1],
                'verbosity': [0, 0, 1]}

#starting mqtt server
try:
    mqtt = Mqtt(app)
    mqtt.subscribe('#')    
except:
    print('unable to start mqtt server')


if len(argv) > 1:
    for arg_index in range(len(argv[:-1])):
        if argv[arg_index] == '--new-sensors-db':
            table_names, message = db.get_list_of_table_names()
            for name in table_names:
                db.drop_table(name[0])
        if argv[arg_index] == '--new-ml-db':
            table_names, message = db.get_list_of_table_names(database_name = 'ml.db')
            for name in table_names:
                db.drop_table(name[0])
            db.query_db('CREATE TABLE IF NOT EXISTS models (id INTEGER UNIQUE PRIMARY KEY, device_name STRING, table_name STRING, trainable STRING, use STRING)', database_name = 'ml.db')


# SCHEDULED TASK SEND TODO
def use_all_models():
    print('one minute has passed, send data to all devices!')
job_use_models = cron.add_job(use_all_models, 'interval', minutes = 1)



# SCHEDULED TASK TRAIN TODO
def train_all_models():
    devices = db.query('SELECT * FROM models', database_name = 'ml.db')
    for device in devices:
        device_name = device[1]
        table_name = device[2]
        trainable = device[3]
        use = device[3]
        print(device_name, table_name, trainable, use)
        data = get('localhost:5000/data/10000/{}'.format(api_token))
        if trainable == 'true':
            automl = AutoTuningHyperparameters(DecisionTreeClassifier, data, XGB_PARAMS, f1_score, forecast = 1, y_rule = device_name)
            model, score = automl.auto_tune_pipeline()
            ml_models[device_name + '_' + table_name] = {'model': model, 'score': score, 'standarization matrix': automl.standarization_matrix}

    with open('./models/devices_rules', 'wb') as devices_rules_file:
        pickle.dump(ml_models, devices_rules_file)
    print('24 hours has passed, train!')

train_all_models() #test use
job_train_models = cron.add_job(train_all_models, 'interval',hours=24)


atexit.register(lambda: cron.shutdown(wait=False))

@app.route('/data/<token>', methods = ['GET'])
def get_data(token):
    if token != api_token:
        return "unathorized connection"
    table_names, message = db.get_list_of_table_names()
    data = {}
    for name in table_names:
        column_names, message = db.get_column_names(name[0])
        data_from_table, message = db.select_all_from_table(name[0])
        data[str(name[0])] = deepcopy([{col_name: data for col_name, data in tuple(zip(column_names, data_row))} for data_row in data_from_table])

    return str(json.dumps(data)), "200"

@app.route('/data/<size>/<token>', methods = ['GET'])
def get_tails(size, token):
    if token != api_token:
        return "unathorized connection"
    table_names, message = db.get_list_of_table_names()
    data = {}
    for name in table_names:
        column_names, message = db.get_column_names(name[0])
        data_from_table, message = db.select_tail(name[0], int(size))
        data[str(name[0])] = deepcopy([{col_name: data for col_name, data in tuple(zip(column_names, data_row))} for data_row in data_from_table])

    return str(json.dumps(data)), "200"

@app.route('/data/<name>/<token>', methods = ['DELETE'])
def delete_table(name, token):
    if token != api_token:
        return "unathorized connection"
    boolean, message = db.drop_table(name)
    if not boolean:
        return str(message), "500"
    return "Success", "200"

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     try:
#         data_from_topic = str(message.payload.decode()).split(' ')
#         date = time.asctime(time.localtime())
#         data = [date] 
#         columns = ['date']
#         table_name = str(message.topic)
#         for index, record in enumerate(data_from_topic):
#             if index % 2 == 0:
#                 columns.append(record)
#             else:
#                 data.append(record)
#         table_names, error_message = db.get_list_of_table_names()
#         if table_name not in [str(name[0]) for name in table_names]:
#             print(table_names)
#             db.create_table(table_name, columns)
#             print('created table ' + table_name)
#             for column in columns:
#                 if 'device' in column:
#                     db.query_db('INSERT INTO models (device_name, table_name, trainable, use) VALUES ("' + column + '","' + table_name + '", "false", "false");', database_name = 'ml.db')
#         db.insert_record_into_table(table_name, data)
#     except Exception as e:
#         print(str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

