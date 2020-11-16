from controller import *

# app and scheduler
app = Flask(__name__)

cron = BackgroundScheduler(daemon=True)
cron.start()

# STATIC CONST VARIABLES

MODEL_USAGE_INTERVAL = 10
MODEL_LEARNING_INTERVAL = 24
TIME_SERIES_SIZE = 3
N_CLUSTERS = 3

mqtt_port = 1885
mqtt_url = '192.168.1.110'

if len(argv) > 1:
    for arg_index in range(len(argv)):
        if argv[arg_index] == '--new-sensors-db':
            table_names, message = db.get_list_of_table_names()
            for name in table_names:
                db.drop_table(name[0])
        if argv[arg_index] == '--new-ml-db':
            table_names, message = db.get_list_of_table_names(database_name = 'ml.db')
            for name in table_names:
                db.drop_table(name[0], database_name = 'ml.db')
            db.query_db('CREATE TABLE models (id INTEGER UNIQUE PRIMARY KEY, device_name STRING, table_name STRING, trainable STRING, use STRING)', database_name = 'ml.db')
        if argv[arg_index] == '-mqtt-port' and arg_index < len(argv) - 1:
            mqtt_port = int(argv[arg_index+1])
        if argv[arg_index] == '-mqtt-url' and arg_index < len(argv) - 1:
            mqtt_url = str(argv[arg_index+1])
        if argv[arg_index] == '-ml-u' and arg_index < len(argv) - 1:
            MODEL_USAGE_INTERVAL = int(argv[arg_index+1])
        if argv[arg_index] == '-ml-l' and arg_index < len(argv) - 1:
            MODEL_LEARNING_INTERVAL = int(argv[arg_index+1])
        if argv[arg_index] == '-tss' and arg_index < len(argv) - 1:
            TIME_SERIES_SIZE = int(argv[arg_index+1])
        if argv[arg_index] == '-n-clusters' and arg_index < len(argv) - 1:
            N_CLUSTERS = int(argv[arg_index+1])
        if argv[arg_index] == '-h':
            print('--new-sensors-db       if provided, creates new database for sensors and devices       example usage: python app.py --new-sensors-db')
            print('--new-ml-db            if provided, creates new database for ml models                 example usage: python app.py --new-ml-db')
            print('-mqtt-port             mqtt broker port                                                example usage: python app.py -mqtt-port 1885')
            print('-mqtt-url              mqtt broker url                                                 example usage: python app.py -mqtt-url 192.168.1.110')
            print('-ml-u                  time interval for using ml models in minutes                    example usage: python app.py -ml-u 10')
            print('-ml-l                  time interval for learning ml models in hours                   example usage: python app.py -ml-l 24')
            print('-tss                   size of the time series that ml model "see"                     example usage: python app.py -tss 3')
            print('-n-clusters            number of behaviour groups that clustering algorithm can find   example usage: python app.py -tss 3')
            print('-h                     help                                                            example usage: python app.py -h')
            exit()

app.config['MQTT_BROKER_URL'] = mqtt_url  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = mqtt_port  # default port for non-tlp connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 20  # set the time interval for sending a ping to the broker to 20 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

# loading ml models
try:
    with open('models/devices_rules', 'rb') as devices_rules_file:
        ml_models = pickle.load(devices_rules_file)
        print(ml_models)
except Exception as e:
    print(e)
    ml_models = {}

try:
    with open('models/behaviours', 'rb') as behaviours_file:
        behaviours = pickle.load(behaviours_file)
        print(behaviours)
except Exception as e:
    print(e)
    behaviours = {'n_clusters': N_CLUSTERS, 'model': None, 'columns': None}

ML_MODEL_PARAMS = { 'max_depth': [3, 300, 30],
               'min_samples_split': [0.1, 1, 0.1],
               'min_samples_leaf': [0.1, 0.5, 0.1]}

# SCHEDULED TASK SEND 
def use_all_models():
    devices = db.query_db('SELECT * FROM models', database_name = 'ml.db')
    data = get('http://localhost:5000/data/4/{}'.format(api_token)).json()
    for device in devices:
        device_name = device[1]
        table_name = device[2]
        trainable = device[3]
        use = device[4]
        print(device_name, table_name, trainable, use)
        if use == 'true' and device_name + '_' + table_name in ml_models.keys():
            X, _ = DataPreprocessor(data, standarization_rule='NO STANDARIZATION').time_series(time_series_size = TIME_SERIES_SIZE, forecast = None, y_rule=device_name)
            for x_column in X.columns:
                for standarization_column in ml_models[device_name + '_' + table_name]['standarization matrix'].columns:
                    if standarization_column in x_column:
                        X.loc[0, x_column] = (X.loc[0, x_column] - ml_models[device_name + '_' + table_name]['standarization matrix'].loc['mean', standarization_column])/ml_models[device_name + '_' + table_name]['standarization matrix'].loc['std', standarization_column]
                        break
            prediction =  ml_models[device_name + '_' + table_name]['model'].predict(X)[0]
            print('time: {} topic: {}, device name: {}, prediction: {}'.format(time.asctime(time.localtime()), table_name, device_name, prediction))
            if mqtt:
                mqtt.publish('control/{}/{}'.format(table_name, device_name), str(prediction))
                print('topic: {}, prediction: {}'.format('control/{}/{}'.format(table_name, device_name), str(prediction)))
            

job_use_models = cron.add_job(use_all_models, 'interval', minutes = MODEL_USAGE_INTERVAL)



# SCHEDULED TASK TRAIN 
def train_all_models():
    devices = db.query_db('SELECT * FROM models', database_name = 'ml.db')
    data = get('http://localhost:5000/data/15000/{}'.format(api_token)).json()
    for device in devices:
        device_name = device[1]
        table_name = device[2]
        trainable = device[3]
        use = device[4]
        print(device_name, table_name, trainable, use)
        if trainable == 'true':
            automl = AutoTuningHyperparameters(DecisionTreeClassifier, data, ML_MODEL_PARAMS, balanced_accuracy_score, time_series_size=TIME_SERIES_SIZE, forecast = 1, y_rule = device_name)
            model, score = automl.auto_tune_pipeline()
            print(score)
            ml_models[device_name + '_' + table_name] = {'model': model, 'score': score, 'standarization matrix': automl.data_preprocessor.standarization_matrix}

    with open('./models/devices_rules', 'wb') as devices_rules_file:
        pickle.dump(ml_models, devices_rules_file)
    print(ml_models)

job_train_models = cron.add_job(train_all_models, 'interval', hours = MODEL_LEARNING_INTERVAL)


# SCHEDULED TASK TRAIN CLUSTERING
def train_clustering():
    data = get('http://localhost:5000/data/15000/{}'.format(api_token)).json()
    data_preprocessor = DataPreprocessor(data)
    X, _ = data_preprocessor.time_series(time_series_size=TIME_SERIES_SIZE, forecast=None)
    model = K_MEAN.Model(X_train = X.to_numpy(), n_clusters=N_CLUSTERS)
    model.fit(epochs = 500, verbose = 0)
    behaviours = {'n_clusters': N_CLUSTERS, 'model': model, 'columns': X.columns}
    with open('./models/behaviours', 'wb') as behaviours_file:
        pickle.dump(behaviours, behaviours_file)
    print(behaviours, model.__centroids__(epoch = 'final'))

job_train_clustering = cron.add_job(train_clustering, 'interval', hours = MODEL_LEARNING_INTERVAL)

atexit.register(lambda: cron.shutdown(wait=False))

####### endpoint data/ #########

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

####### endpoint rules/ #########

@app.route('/rules/<token>', methods = ['GET'])
def get_models_names(token):
    if token != api_token:
        return "unathorized connection"
    
    models_names = list(ml_models.keys())

    return str(json.dumps(models_names)), "200"

@app.route('/rules/<name>/<token>', methods = ['GET'])
def get_model(name, token):
    if token != api_token:
        return "unathorized connection"
    
    try:
        model = ml_models[name]
    except:
        return "model not found", "404"

    buffer = io.BytesIO()
    fig = figure(figsize=(6,3), dpi=300)
    feature_names = []
    for i in range(TIME_SERIES_SIZE):
        feature_names += [feature_name + '_' + str(i) for feature_name in list(model['standarization matrix'].columns)]
    viz = plot_tree(model['model'], feature_names=feature_names, filled=True, class_names=["ON", "OFF"])
    fig.savefig(buffer)
    close(fig)
    viz = buffer.getvalue().decode('ISO-8859-1')
    model = {'model_graph': viz, 'score': model['score'],
            'features': {'names': list(model['standarization matrix'].columns), 
                        'standarized': model['standarization matrix'].values.tolist()}}
    return json.dumps(model), "200"

# starting mqtt server
try:
    mqtt = Mqtt(app)
    mqtt.subscribe('#')

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        try:
            if 'control/' in str(message.topic):
                return

            if 'data/' in str(message.topic):
                data_from_topic = str(message.payload.decode()).split(' ')
                date = time.asctime(time.localtime())
                data = [date] 
                columns = ['date']
                table_name = str(message.topic).replace('data/', '')
                for index, record in enumerate(data_from_topic):
                    if index % 2 == 0:
                        columns.append(record)
                    else:
                        data.append(record)
                table_names, error_message = db.get_list_of_table_names()
                if table_name not in [str(name[0]) for name in table_names]:
                    print(table_names)
                    db.create_table(table_name, columns)
                    print('created table ' + table_name)
                    for column in columns:
                        if 'device' in column:
                            db.query_db('INSERT INTO models (device_name, table_name, trainable, use) VALUES ("' + column + '","' + table_name + '", "false", "false");', database_name = 'ml.db') 
                db.insert_record_into_table(table_name, data)
            
            elif 'model/' in str(message.topic):
                table_name, device_name = str(message.topic).replace('model/', '').split('/')
                data_from_topic = str(message.payload.decode()).split(' ')
                train = data_from_topic[0]
                use = data_from_topic[1]
                db.query_db('UPDATE models Set trainable = "' + train + '" , use = "' + use + '" WHERE device_name = "' + device_name + '" AND table_name = "' + table_name + '";', database_name = 'ml.db')

        except Exception as e:
            print(str(e))    

except:
    print('unable to start mqtt server')
    mqtt = None





if __name__ == '__main__':
    app.run(debug=False, port=5000)

