try:    
    from Src.controller import *
except:
    from controller import *

if len(argv) > 1:
    if argv[1] == '--new-db':
        table_names, message = db.get_list_of_table_names()
        for name in table_names:
            db.drop_table(name[0])

@app.route('/data/<token>', methods = ['GET'])
def get_data(token):
    if token != api_token:
        return "unathorized connection"
    table_names, message = db.get_list_of_table_names()
    data = {}
    for name in table_names:
        column_names = db.get_column_names(name[0])
        data_from_table, message = db.select_all_from_table(name[0])
        data[str(name[0])] = deepcopy([{col_name: data for col_name, data in list(zip(column_names, data_row))} for data_row in data_from_table])

    return str(json.dumps(data)), "200"

@app.route('/data/<size>/<token>', methods = ['GET'])
def get_tails(size, token):
    if token != api_token:
        return "unathorized connection"
    table_names, message = db.get_list_of_table_names()
    data = {}
    for name in table_names:
        column_names = db.get_column_names(name[0])
        data_from_table, message = db.select_tail(name[0], int(size))
        data[str(name[0])] = deepcopy([{col_name: data for col_name, data in list(zip(column_names, data_row))} for data_row in data_from_table])

    return str(json.dumps(data)), "200"

@app.route('/data/<name>/<token>', methods = ['DELETE'])
def delete_table(name, token):
    if token != api_token:
        return "unathorized connection"
    boolean, message = db.drop_table(name)
    if not boolean:
        return str(message), "500"
    return "Success", "200"

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        data_from_topic = str(message.payload.decode()).split(' ')
        date = time.asctime(time.localtime())
        data = [date] 
        columns = ['date']
        table_name = str(message.topic)
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
        db.insert_record_into_table(table_name, data)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

