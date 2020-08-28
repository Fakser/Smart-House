from Src.controller import *
from Src.Objects.ESP_room_1 import *

if len(argv) > 1:
    if argv[1] == '--new-db':
        db.create_all()

@app.route('/data', methods = ['GET'])
def get_data():
    """
    Endpoint that returns all data in database
    """
    return jsonify(esp_room_1_schema_multiple.dump(ESP_room_1.query.all())), "200"


@app.route('/data', methods = ['POST'])
def add_data():
    """
    Endpoint that returns all data in database
    """
    try:
        date = request.json['date']
        sensor_1 = request.json['sensor_1']
        sensor_2 = request.json['sensor_2']
        device_1 = request.json['device_1']
    except:
        return "key error, proper keys not found", "404"
    try:    
        new_reading = ESP_room_1(date, sensor_1, sensor_2, device_1)
        db.session.add(new_reading)
        db.session.commit()
    except Exception as e:
        return str(e), "500"
    return jsonify(esp_room_1_schema.dump(new_reading)), '200' 


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(topic=message.topic, payload=message.payload.decode())
    print('hello', data)

if __name__ == '__main__':
    app.run(debug=True)