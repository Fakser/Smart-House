try:    
    from Src.controller import *
except:
    from controller import *

if len(argv) > 1:
    if argv[1] == '--new-db':
        table_names, message = db.get_list_of_table_names()
        for name in table_names:
            db.drop_table(name[0])


@app.route('/data', methods = ['GET'])
def get_data():
    table_names, message = db.get_list_of_table_names()
    # if not table_names:
    #     return str(message), "500"
    data = {}
    for name in table_names:
        data_from_table, message = db.select_all_from_table(name[0])
        # if not data_from_table:
        #     return str(message), "500"
        data[str(name[0])] = deepcopy(data_from_table)

    return str(json.dumps(data)), "200"

@app.route('/data/<size>', methods = ['GET'])
def get_tails(size):
    table_names, message = db.get_list_of_table_names()
    # if not table_names:
    #     return str(message), "500"
    data = {}
    for name in table_names:
        data_from_table, message = db.select_tail(name[0], int(size))
        # if not data_from_table:
        #     return str(message), "500"
        data[str(name[0])] = deepcopy(data_from_table)

    return str(json.dumps(data)), "200"

@app.route('/data/<name>', methods = ['DELETE'])
def delete_table(name):
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
        if not table_names:
            return str(error_message), "500"
        if table_name not in [str(name[0]) for name in table_names]:
            db.create_table(table_name, columns)
            print('created table ' + table_name)
        db.insert_record_into_table(table_name, data)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    app.run(debug=True)

