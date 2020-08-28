from Src.controller import *

class ESP_room_1(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(100))
    sensor_1 = db.Column(db.String(10))
    sensor_2 = db.Column(db.String(10))
    device_1 = db.Column(db.String(10))

    def __init__(self, date, sensor_1, sensor_2, device_1):
        self.date = date
        self.sensor_1 = sensor_1
        self.sensor_2 = sensor_2
        self.device_1 = device_1

    def __repr__(self):
        return '<SQLite table representing all data>'
    

class ESP_room_1_Schema(ma.Schema):
    class Meta:
        fields = ("id", "date", "sensor_1",  "sensor_2",  "device_1")


esp_room_1_schema = ESP_room_1_Schema() #schema for one reading
esp_room_1_schema_multiple = ESP_room_1_Schema(many=True) #schema for many readings